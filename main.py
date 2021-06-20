from sklearn.metrics.pairwise import pairwise_distances
from tensorflow.python.platform import gfile
import tensorflow as tf
import numpy as np
import detect_and_align
import argparse
import time
import cv2
import os
import datetime

import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
#from RegistrationPage import RegistrationPage
import webbrowser
import random


class IdData:
    """Keeps track of known identities and calculates id matches"""

    def __init__(
        self, id_folder, mtcnn, sess, embeddings, images_placeholder, phase_train_placeholder, distance_treshold
    ):
        print("Loading known identities: ", end="")
        self.distance_treshold = distance_treshold
        self.id_folder = id_folder
        self.mtcnn = mtcnn
        self.id_names = []

        image_paths = []
        ids = os.listdir(os.path.expanduser(id_folder))
        for id_name in ids:
            id_dir = os.path.join(id_folder, id_name)
            image_paths = image_paths + [os.path.join(id_dir, img) for img in os.listdir(id_dir)]

        print("Found %d images in id folder" % len(image_paths))
        aligned_images, id_image_paths = self.detect_id_faces(image_paths)
        feed_dict = {images_placeholder: aligned_images, phase_train_placeholder: False}
        self.embeddings = sess.run(embeddings, feed_dict=feed_dict)

        if len(id_image_paths) < 5:
            self.print_distance_table(id_image_paths)

    def detect_id_faces(self, image_paths):
        aligned_images = []
        id_image_paths = []
        for image_path in image_paths:
            image = cv2.imread(os.path.expanduser(image_path), cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_patches, _, _ = detect_and_align.detect_faces(image, self.mtcnn)
            if len(face_patches) > 1:
                print(
                    "Warning: Found multiple faces in id image: %s" % image_path
                    + "\nMake sure to only have one face in the id images. "
                    + "If that's the case then it's a false positive detection and"
                    + " you can solve it by increasing the thresolds of the cascade network"
                )
            aligned_images = aligned_images + face_patches
            id_image_paths += [image_path] * len(face_patches)
            path = os.path.dirname(image_path)
            self.id_names += [os.path.basename(path)] * len(face_patches)

        return np.stack(aligned_images), id_image_paths

    def print_distance_table(self, id_image_paths):
        """Prints distances between id embeddings"""
        distance_matrix = pairwise_distances(self.embeddings, self.embeddings)
        image_names = [path.split("/")[-1] for path in id_image_paths]
        '''''
        print("Distance matrix:\n{:20}".format(""), end="")
        [print("{:20}".format(name), end="") for name in image_names]
        for path, distance_row in zip(image_names, distance_matrix):
            print("\n{:20}".format(path), end="")
            for distance in distance_row:
                print("{:20}".format("%0.3f" % distance), end="")
        print()
        '''''

    def find_matching_ids(self, embs):
        matching_ids = []
        matching_distances = []
        distance_matrix = pairwise_distances(embs, self.embeddings)
        for distance_row in distance_matrix:
            min_index = np.argmin(distance_row)
            if distance_row[min_index] < self.distance_treshold:
                matching_ids.append(self.id_names[min_index])
                matching_distances.append(distance_row[min_index])
            else:
                matching_ids.append(None)
                matching_distances.append(None)
        return matching_ids, matching_distances


def load_model(model):
    model_exp = os.path.expanduser(model)
    if os.path.isfile(model_exp):
        print("Loading model filename: %s" % model_exp)
        with gfile.FastGFile(model_exp, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name="")
    else:
        raise ValueError("Specify model file, not directory!")


def main(model, id_folder, threshold):
    with tf.Graph().as_default():
        with tf.Session() as sess:

            # Setup models
            mtcnn = detect_and_align.create_mtcnn(sess, None)
            load_model(model)
            #load_model(args.model)
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            # Load anchor IDs
            id_data = IdData(
                #args.id_folder[0],
                id_folder,
                mtcnn,
                sess,
                embeddings,
                images_placeholder,
                phase_train_placeholder,
                #args.threshold,
                threshold,
            )

            cap = cv2.VideoCapture(0)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            show_landmarks = False
            show_bb = False
            show_id = True
            show_fps = False
            col_names =  ['Name','Date','Time']
            attendance = pd.DataFrame(columns = col_names)
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            while True:
                start = time.time()
                _, frame = cap.read()

                # Locate faces and landmarks in frame
                face_patches, padded_bounding_boxes, landmarks = detect_and_align.detect_faces(frame, mtcnn)

                if len(face_patches) > 0:
                    face_patches = np.stack(face_patches)
                    feed_dict = {images_placeholder: face_patches, phase_train_placeholder: False}
                    embs = sess.run(embeddings, feed_dict=feed_dict)
                    matching_ids, matching_distances = id_data.find_matching_ids(embs)

                    for bb, landmark, matching_id, dist in zip(
                        padded_bounding_boxes, landmarks, matching_ids, matching_distances
                    ):
                        if matching_id is None:
                            matching_id = "Unknown"
                        elif matching_distances[0] is not None:
                            #print(matching_distances)
                            if matching_distances[0] > .70:
                                matching_id = "Unknown"
                        #else:
                        #    print("Hi %s! Distance: %1.4f" % (matching_id, dist))
                        #show_id:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, matching_id, (bb[0], bb[3]), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = matching_id
                        #print("Name : ", aa)
                        #tt=str(Id)+"-"+aa
                        attendance.loc[len(attendance)] = [aa,date,timeStamp]
                        #print("attendance, ", attendance)
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        Hour,Minute,Second=timeStamp.split(":")
                        #myCsvRow =
                        #with open('Attendance\Attendance.csv','a') as fd:
                            #fd.write(attendance)
                        fileName="Attendance\Attendance.csv"
                        attendance.to_csv(fileName, mode='a', index=True)
                        res=attendance
                        cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), (255, 0, 0), 2)
                        if show_landmarks:
                            for j in range(5):
                                size = 1
                                top_left = (int(landmark[j]) - size, int(landmark[j + 5]) - size)
                                bottom_right = (int(landmark[j]) + size, int(landmark[j + 5]) + size)
                                cv2.rectangle(frame, top_left, bottom_right, (255, 0, 255), 2)
                #else:
                #    print("Couldn't find a face")

                end = time.time()

                seconds = end - start
                fps = round(1 / seconds, 2)

                if show_fps:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(fps), (0, int(frame_height) - 5), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.imshow("frame", frame)

                key = cv2.waitKey(1)
                if key == ord("q"):
                    break
                elif key == ord("l"):
                    show_landmarks = not show_landmarks
                elif key == ord("b"):
                    show_bb = not show_bb
                elif key == ord("i"):
                    show_id = not show_id
                elif key == ord("f"):
                    show_fps = not show_fps

            cap.release()
            cv2.destroyAllWindows()