import tkinter as tk
from tkinter import *
from tkinter import Message ,Text
import cv2
import os
import shutil
import tkinter.font as font
#from RegistrationPage import RegistrationPage
import webbrowser
import random
#from main import main

window = tk.Tk()
mobileNo = 1234
email = 'abc@gmail.com'

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Identification")

#dialog_title = 'QUIT'
#dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

# this removes the maximize button
window.resizable(0,0)
window_height = 600
window_width = 880

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
#window.geometry('880x600')
window.configure(background='#ffffff')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#var = StringVar(window)
#var.set("Faculty") # initial value

#desg = tk.Label(window, text="Role :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
#desg.place(x=80, y=200)
'''
genderVar = StringVar(window)
genderVar.set("Male") # initial value

gender = tk.Label(window, text="Gender :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
gender.place(x=80, y=140)

genderVal = OptionMenu(window, genderVar, "Male", "Female", "Others")
genderVal.config(width=18)
genderVal.config(font=27)
genderVal.place(x=205, y=140)'''

#message = tk.Label(window, text="Face-Recognition Attendance" ,bg="White"  ,fg="black"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline'))

#message.place(x=200, y=20)
def manipulateFont(*args):
    newFont = (font.get(), fontSize.get())
    return newFont

def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)

def takeImages():
    Id=(idTxt.get())
    name=(stNameTxt.get())
    
    if (Id or name):
        
        if os.path.isdir("ids/" + name):
            shutil.rmtree("ids/" + name)
        else:
            os.mkdir("ids/" + name)
        if(is_number(Id) and is_number(mobileNo)):
            cam = cv2.VideoCapture(0)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #incrementing sample number
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("ids/"+name+"\\"+name +"."+Id +'.'+ str(sampleNum) + ".jpg", img)
                #display the frame
                cv2.imshow('frame',img)
                #wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>20:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name, mobileNo, email]
    
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
                if(name.isalpha()):
                    res = "Enter Numeric Id"
                    message.configure(text= res)
                    
    else:
        #res = "Please provide valid ID and Name"
        message.configure(text = "Please provide valid ID and Name")
         
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

                
'''def trackImages():
     model = "models/20170512-110547.pb"
     id_folder = "ids"
     threshold = 1.2
     main(model, id_folder, threshold)'''

def close_window ():
    window.destroy()

def callback(url):
    webbrowser.open_new(url)
                        
    
def getRandomNumber():
    ability = str(random.randint(1,10))
    updateDisplay(ability)

def updateDisplay(myString):
    displayVariable.set(myString)

header = tk.Label(window, text="Face Capturing System",width=70  ,height=2  ,fg="white"  ,bg="#17a2b8" ,font=('times', 18, 'bold', 'underline') )
header.place(x=0, y=0)
stId = tk.Label(window, text="User ID",width=10  ,height=1  ,fg="white"  ,bg="#17a2b8" ,font=('times', 15) )
stId.place(x=80, y=80)

displayVariable = StringVar()
idTxt = tk.Entry(window,width=20 , text=displayVariable ,bg="white" ,fg="black",font=('times', 15, ' bold '))
idTxt.place(x=205, y=80)


stName = tk.Label(window, text="Name",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
stName.place(x=450, y=80)

stNameTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
stNameTxt.place(x=575, y=80)

#mblNo = tk.Label(window, text="Mobile No:",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
#mblNo.place(x=80, y=140)
    
#mblNoTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
#mblNoTxt.place(x=205, y=140)
    
#emailId = tk.Label(window, text="Email ID :",width=10  ,fg="white"  ,bg="#17a2b8",height=1 ,font=('times', 15))
#emailId.place(x=450, y=140)
    
#emailTxt = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold ')  )
#emailTxt.place(x=575, y=140)


lbl3 = tk.Label(window, text="Notification : ",width=10  ,fg="white"  ,bg="#17a2b8"  ,height=1 ,font=('times', 15, 'underline '))
lbl3.place(x=80, y=260)

message = tk.Label(window, text="" ,bg="#bbc7d4"  ,fg="black"  ,width=52  ,height=1, activebackground = "#bbc7d4" ,font=('times', 15))
message.place(x=205, y=260)

'''
lbl3 = tk.Label(window, text="Attendance : ",width=10  ,fg="white"  ,bg="#17a2b8"  ,height=2 ,font=('times', 15, 'underline'))
lbl3.place(x=80, y=440)

message2 = tk.Label(window, text="" ,fg="#e47911"   ,bg="#bbc7d4",activeforeground = "#f8f9fa",width=52  ,height=2  ,font=('times', 15))
message2.place(x=205, y=440)
'''

takeImg = tk.Button(window, text="Take Images",  command=takeImages, fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
takeImg.place(x=80, y=350)
#trainImg = tk.Button(window, text="Train Images", fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
#trainImg.place(x=333, y=350)

'''trackImg = tk.Button(window, text="Face identification", command=trackImages, fg="white"  ,bg="#17a2b8"  ,width=15  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
trackImg.place(x=580, y=350)


quitWindow = tk.Button(window, text="Quit", command=close_window  ,fg="white"  ,bg="#17a2b8"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
quitWindow.place(x=650, y=510)
'''
quitWindow = tk.Button(window, text="Quit", command=close_window  ,fg="white"  ,bg="#17a2b8"  ,width=10  ,height=1, activebackground = "#118ce1" ,font=('times', 15, ' bold '))
quitWindow.place(x=650, y=510)

link2 = tk.Label(window, text="Copyright ?? 2020, Unilever", fg="blue", )
link2.place(x=720, y=580)
#link2.pack()
link2.bind("<Button-1>", lambda e: callback("http://unilever.com"))
label = tk.Label(window)  

#app=FullScreenApp(window)
window.mainloop()
