############################################# IMPORTING ################################################
import csv
import datetime

import time
import tkinter as tk
import tkinter.simpledialog as tsd
from tkinter import *
from tkinter import Label
from tkinter import messagebox
from tkinter import messagebox as mess
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import threading
import cv2
import numpy as np
import os
import pandas as pd
import pyttsx3
from PIL import Image
from PIL import ImageTk
import speech_recognition as sr

###########################################################################################
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
###########################################################################################
def tick():
    time_string = time.strftime('%I:%M:%S %p')
    clock.config(text=time_string)
    clock.after(200,tick)

###########################################################################################
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some files are missing', message='Please contact us for help')
        window.destroy()

###########################################################################################
def func(event):
    psw()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    password = PSW_INP.get()
    if (password == key):
        show_frame(MainPage)
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
        clear()
###########################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()
    ###########################################################################################
def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='Enter Old Password',bg='white',font=('Century Gothic', 10 ))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('Century Gothic', 11),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='Enter New Password', bg='white', font=('Century Gothic', 10))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('Century Gothic', 11),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('Century Gothic', 10))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('Century Gothic', 11),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="White"  ,bg="#111211" ,height=1,width=20 , activebackground = "white" ,font=('Century Gothic', 10))
    cancel.place(x=205, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="White", bg="#614f41", height = 1,width=20, activebackground="white", font=('Century Gothic', 10))
    save1.place(x=20, y=120)
    master.mainloop()

    ###########################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.','','CLASS', '', 'ID', '', 'NAME']
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists:
        with open("EmployeeDetails\EmployeeDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("EmployeeDetails\EmployeeDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    Class = (txt5.get())

    if ((name.isalpha()) or (' ' in name)):
        if ((Id.isnumeric()) or (' ' in Id)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            face_detected = False

            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                if len(faces) == 0:
                    cv2.putText(img, "Face not detected. Please use proper lighting.", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                for (x, y, w, h) in faces:
                    face_detected = True
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w], [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                cv2.imshow('Taking Images', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            if not face_detected:
                print("Face not detected. Please use proper lighting and try again.")
                TakeImages()
            else:
                row = [serial,'',Class,'', Id, '', name]
                with open('EmployeeDetails\EmployeeDetails.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
        else:
            if (name.isalpha() == False):
                Popup = Label(Registerpage, text="Enter Correct Name", font=("Century Gothic", 18), bg="#d0d3d4",
                              width=21, height=1)
                Popup.place(x=167, y=490)
                Popup.after(2400, Popup.destroy)
            elif (Id.isalpha() == True):
                Popup = Label(Registerpage, text="Enter Correct Roll Number", font=("Century Gothic", 18),
                              bg="#d0d3d4",
                              width=21, height=1)
                Popup.place(x=167, y=500)
                Popup.after(2400, Popup.destroy)


########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    mess._show(title='Registration',
               message="Employee Registered Sucessfully")


############################################################################################3

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def show_temporary_message(window, title, message, duration):

    messagebox.showinfo(title, message, parent=window)
    t = threading.Timer(duration / 1000, show_temporary_message())
    t.start()


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen_and_write_to_file():
    start_thread1 = threading.Thread(target=listen())
    start_thread1.start()

def listen():
    """Record and process audio."""
    print(" Recognizing.......")
    recognizer_audio = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer_audio.record(source, duration=8)
    try:
        text = recognizer_audio.recognize_google(audio)
        ts = time.time()
        time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %I:%M:%S %p')
        with open('unregistered_requests.txt', 'a') as f:
            f.write(f"Date and Time: {time_stamp}, Request: {text}\n")
        speak_text("Your concern has been acknowledged. Thank you!. Please move forward.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def starttrack():
    start_thread = threading.Thread(target=TrackImages())
    start_thread.start()


def threaded_speak_text(text):
    """Run the speak_text function in a separate thread."""
    t = threading.Thread(target=speak_text, args=(text,))
    t.start()

def threaded_listen_and_write():
    """Run the listen_and_write_to_file function in a separate thread."""
    t = threading.Thread(target=listen_and_write_to_file)
    t.start()

def TrackImages():
    """Track and recognize faces."""
    assure_path_exists("Attendance/")
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImageLabel/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    if not os.path.isfile("EmployeeDetails/EmployeeDetails.csv"):
        mess.showwarning('Details Missing', 'Employee details are missing, please check!')
        return
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess.showwarning('Data Missing', 'Please click on Save Profile to reset data!!')
        return

    df = pd.read_csv("EmployeeDetails/EmployeeDetails.csv")
    recognizer.read("TrainingImageLabel/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    file_name = f"Attendance/Attendance_{date}.csv"
    exists = os.path.isfile(file_name)
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    last_recognized_name = None
    last_unrecognized_time = 0

    frame_counter = 0
    FRAME_SKIP = 5  # Regular frame skip
    UNRECOGNIZED_FRAME_SKIP = 10 * 30  # Skip for 10 seconds (assuming 30fps)
    skip_frames = FRAME_SKIP

    # Create a dictionary for faster lookups
    data_dict = df.set_index('SERIAL NO.').to_dict(orient='index')

    with open(file_name, 'a+') as csvFile1:
        writer = csv.writer(csvFile1)
        if not exists:
            writer.writerow(col_names)

        while True:
            ret, im = cam.read()

            # Reduce frame size for faster face detection
            small_frame = cv2.resize(im, (0, 0), fx=0.5, fy=0.5)

            frame_counter += 1
            if frame_counter % skip_frames != 0:
                continue

            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            recognized = False

            for (x, y, w, h) in faces:
                x, y, w, h = x*2, y*2, w*2, h*2  # Scale coordinates back to original frame size
                bb = "Not Registered"
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 225, 0), 2)
                serial, conf = recognizer.predict(gray[y//2:y//2 + h//2, x//2:x//2 + w//2])

                if (conf > 35) and (serial in data_dict):
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
                    bb = data_dict[serial]['NAME']
                    ID = data_dict[serial]['ID']
                    if bb != last_recognized_name:
                        last_recognized_name = bb
                        threaded_speak_text(f"Hello {bb}! Welcome, your attendance has been recorded.")
                        attendance = (str(ID), '', bb, '', str(date), '', str(timeStamp))
                        writer.writerow(attendance)
                    recognized = True
                else:
                    current_time = time.time()
                    if current_time - last_unrecognized_time > 10:
                        last_unrecognized_time = current_time
                        threaded_speak_text("Hello! How can I help you?")
                        threaded_listen_and_write()

                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)

            if not recognized:
                skip_frames = UNRECOGNIZED_FRAME_SKIP
            else:
                skip_frames = FRAME_SKIP

            cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q')):
                break

        cam.release()
        cv2.destroyAllWindows()

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {'01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }


def clear():
    txt.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input an ID Number", font=("Century Gothic ", 13), bg="#fff",width=22,height=1)
    busted_display.place(x=140, y=235)
    window.after(2400, busted_display.destroy)

def clear2():
    txt2.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input A Name", font=("Century Gothic",13), bg="#fff", width=21, height=1)
    busted_display.place(x=140, y=334)
    window.after(2400, busted_display.destroy)


def clear4():
    PSW_INP.delete(0, 'end')

def clear5():
    txt5.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    busted_display = Label(Registerpage, text="Please Input A Faculty", font=("Century Gothic", 13), bg="#fff", width=21,
                           height=1)
    busted_display.place(x=140, y=425)
    window.after(2400, busted_display.destroy)
###########################################################################################
def contact():
    mess._show(title='Contact us', message="Please contact us at : raj123@gmail.com ")

def confirm1():
    answer = askyesno(title='Logout', message='Are you sure that you want to logout?')
    if answer:
        show_frame(Startup)
    PSW_INP.delete(0, 'end')
def confirm2():
    answer = askyesno(title='Quit', message='Are you sure that you want to Quit?')
    if answer:
        window.destroy()
def show_frame(frame):
    frame.tkraise()
###########################################################################################

################################ TEXBOX & LABELS ##################################

window = tk.Tk()
window.geometry("1366x768")
window.resizable(False,False)
window.title("RECOGNITO")
window.rowconfigure(0,weight=1)
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='icon.png'))

filename = ImageTk.PhotoImage(Image.open('Background.jpg' ))
###################################################--------------------STARTUP PAGE----------############################################################
Startup = tk.Frame(window)
Startup.grid(row=0,column=0,stick='nsew')

background_image_path = "Background1.jpg"
image = Image.open(background_image_path)
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(Startup, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Styling constants
btn_bg = "#555555"  # Dark grey
btn_fg = "#FFFFFF"  # White
btn_active_bg = "#444444"
btn_font = ('Century Gothic', 15)
entry_font = ('Century Gothic', 28)

# Password Label and Entry
Enter_PSW = tk.Label(Startup, text="Enter Password:", bg="#555555", fg="white", width=20, height=1, font=btn_font)
Enter_PSW.place(x=535, y=330)

PSW_INP = tk.Entry(Startup, width=25, fg="black", relief='solid', font=entry_font, show='*')
PSW_INP.place(x=430, y=370)
PSW_INP.bind('<Return>', func)

# Buttons
login = tk.Button(Startup, text="LOGIN", command=psw, fg=btn_fg, bg=btn_bg, width=20, height=1, activebackground=btn_active_bg, font=btn_font)
login.place(x=430, y=450)

Forget = tk.Button(Startup, text="Forgot?", command=contact, fg=btn_fg, bg=btn_bg, width=20, activebackground=btn_active_bg, font=btn_font)
Forget.place(x=740, y=450)

clearButton = tk.Button(Startup, text="Clear", command=clear4, fg="White", bg="#333333", width=8, activebackground=btn_active_bg, font=('Century Gothic', 18))
clearButton.place(x=860, y=367)



########################################################--------MAIN MENU PAGE############################################################################

MainPage = tk.Frame(window, width= 1366 , height= 768)
MainPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(MainPage, image=filename, bg="#333333")  # Dark background
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Button styling
btn_bg = "#555555"  # Dark grey
btn_fg = "#FFFFFF"  # White
btn_active_bg = "#444444"
btn_font = ('Century Gothic', 12, 'bold')

# Buttons
button1 = Button(MainPage, text="Register Employee", font=btn_font, command=lambda : show_frame(Registerpage),
                 relief=RAISED, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=25, height=2)
button1.place(x=200, y=150)

button2 = Button(MainPage, text="Attendance", font=btn_font, command=lambda : show_frame(TakeattdPage),
                 relief=RAISED, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=25, height=2)
button2.place(x=200, y=230)

button3 = Button(MainPage, text="View Attendance", font=btn_font, command=lambda : [show_frame(ViewPage), viewtablee()],
                 relief=RAISED, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=25, height=2)
button3.place(x=200, y=310)

button4 = Button(MainPage, text="Unregistered Requests", font=btn_font, command=lambda : show_frame(endPage),
                 relief=RAISED, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=25, height=2)
button4.place(x=200, y=390)

button5 = Button(MainPage, text="Log Out", font=btn_font, command=lambda : confirm1(),
                 bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=20, height=2)
button5.place(x=1100, y=600)

button6 = Button(MainPage, text="Quit", font=btn_font, command=lambda : confirm2(),
                 bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=20, height=2)
button6.place(x=1100, y=670)

button8 = Button(MainPage, text="Change Password", font=btn_font, command=lambda : change_pass(),
                 bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=20, height=2)
button8.place(x=1100, y=530)

button9 = Button(MainPage, text="View Employees", font=btn_font, command=lambda : [show_frame(EmpPage), viewtable1()],
                 relief=RAISED, bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, width=25, height=2)
button9.place(x=200, y=470)

datef = tk.Label(MainPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#444444",height=1,font=('Century Gothic', 25))
datef.place(x=760,y=390)

clock = tk.Label(MainPage, fg="white", bg="#262523", height=1, font=('Century Gothic', 25))
clock.place(x=1000, y=70)
tick()

#################################--------------REGISTER PAGE------------------############################################################
Registerpage = tk.Frame(window, width= 1366 , height= 768)
Registerpage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(Registerpage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Regframe = tk.Frame(Registerpage, bg="#D0D3D4")
Regframe.place(relx=0.05, rely=0.17, relwidth=0.38, relheight=0.80)

head2 = tk.Label(Regframe, text="                     New Employee Registration                         ", fg="White",bg="#424949" ,font=('Century Gothic', 17), height=1)
head2.place(x=0,y=0)

lbl = tk.Label(Regframe, text="Enter Roll number:",width=20  ,height=1  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18) )
lbl.place(x=-10, y=55)

txt = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19))
txt.place(x=37, y=100)

lbl3 = tk.Label(Regframe, text="Enter Faculty:",width=20  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18))
lbl3.place(x=-42, y=255)

txt5 = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19))
txt5.place(x=37, y=288)

lbl2 = tk.Label(Regframe, text="Enter Name:",width=20  ,fg="black"  ,bg="#D0D3D4" ,font=('Century Gothic', 18))
lbl2.place(x=-42, y=165)

txt2 = tk.Entry(Regframe,width=32 ,fg="black",font=('Century Gothic', 19)  )
txt2.place(x=37, y=200)

takeImg = tk.Button(Regframe, text="➔ Take Images", command=TakeImages  ,fg="white"  ,bg="#444444"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
takeImg.place(x=45, y=355)

trainImg = tk.Button(Regframe, text="➔ Register Employee", command=TrainImages,fg="white"  ,bg="#444444"  ,width=34  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trainImg.place(x=45, y=430)

datef = tk.Label(Registerpage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#444444" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(Registerpage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

clearButton = tk.Button(Regframe, text="Clear", command=clear  ,fg="White"  ,bg="#111211"  ,width=12 ,activebackground = "white" ,font=('Century Gothic', 14))
clearButton.place(x=350, y=97)
clearButton2 = tk.Button(Regframe, text="Clear", command=clear2  ,fg="White"  ,bg="#111211"  ,width=12 , activebackground = "white" ,font=('Century Gothic', 14))
clearButton2.place(x=350, y=195)
clearButton3 = tk.Button(Regframe, text="Clear", command=clear5  ,fg="White"  ,bg="#111211"  ,width=12 , activebackground = "white" ,font=('Century Gothic', 14))
clearButton3.place(x=350, y=289)
###############################------------------TAKE ATTENDANCE PACE--------------------###################################################
TakeattdPage = tk.Frame(window, width= 1366 , height= 768)
TakeattdPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(TakeattdPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Takeattd = tk.Frame(TakeattdPage, bg="#D0D3D4")
Takeattd.place(relx=0.05, rely=0.25, relwidth=0.38, relheight=0.50)

message1 = tk.Label(Takeattd, text="Steps to Take Attendance:" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message1.place(x=0, y=0)

message2 = tk.Label(Takeattd, text="➜ Click on Take Attendance after each" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message2.place(x=0, y=40)

message3 = tk.Label(Takeattd, text="individual attendance is registered" ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message3.place(x=0, y=65)

trackImg = tk.Button(TakeattdPage, text="Take Attendance", command=lambda: starttrack() ,fg="White"  ,bg="#444444"  ,width=30  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
trackImg.place(x=145,y=480)

back = tk.Button(TakeattdPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#444444"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

datef = tk.Label(TakeattdPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#444444" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

##################################------------------VIEW ATTENDANCE PAGE ----------------########################################################
ViewPage = tk.Frame(window, width= 1366 , height= 768)
ViewPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(ViewPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Viewframe = tk.Frame(ViewPage, bg="#D0D3D4")
Viewframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.60)

def viewtablee():
    tv= ttk.Treeview(Viewframe,height =13,columns = ('name','date','time'))
    tv.column('#0',width=82)
    tv.column('name',width=130)
    tv.column('date',width=133)
    tv.column('time',width=133)
    tv.grid(row=2,column=0,padx=(17,0),pady=(150,0),columnspan=4)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME' )
    scroll = ttk.Scrollbar(Viewframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
            i = 0
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
        csvFile1.close()

message = tk.Label(Viewframe, text="Attendance For the Date: " + date  ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message.place(x=20, y=40)

datef = tk.Label(ViewPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#444444" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(ViewPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#D0D3D4"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

#####################################-----------VIEW Employee PAGE----------------##############################################################
EmpPage = tk.Frame(window, width= 1366 , height= 768)
EmpPage.grid(row=0,column=0,stick='nsew')
background_label = tk.Label(EmpPage, image=filename, bg="#444444")  # Dark background
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Empframe = tk.Frame(EmpPage, bg="#D0D3D4")  # Slightly lighter background for the frame
Empframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.60)


def viewtable1():
    tv = ttk.Treeview(Empframe, height=13, columns=('class', 'roll', 'name'))
    tv.column('#0', anchor=CENTER, width=82)
    tv.column('class', anchor=CENTER, width=130)
    tv.column('roll', anchor=CENTER, width=133)
    tv.column('name', anchor=CENTER, width=133)
    tv.grid(row=2, column=0, padx=(17, 0), pady=(150, 0), columnspan=4)
    tv.heading('#0', text='ID')
    tv.heading('name', text='NAME')
    tv.heading('roll', text='ROLL NUMBER')
    tv.heading('class', text='Faculty')

    scroll = ttk.Scrollbar(Empframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists:
        all_rows = []
        with open("EmployeeDetails\EmployeeDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            next(reader1)  # Skip the header row
            for lines in reader1:
                # Check if the line is empty or doesn't have the expected number of columns
                if len(lines) < 7 or not any(lines):
                    continue
                all_rows.append(lines)

        # Insert rows into the Treeview in reverse order
        for lines in reversed(all_rows):
            iidd = str(lines[0]) + '   '
            tv.insert('', 'end', text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
message = tk.Label(Empframe, text="Registered Employee Info", bg="#444444", fg="white", width=39, height=1, font=('Century Gothic', 15))
message.place(x=20, y=40)

datef = tk.Label(EmpPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="#D0D3D4", bg="#444444", height=1, font=('Century Gothic', 25))
datef.place(x=760,y=390)  # Slightly repositioned for better aesthetics

# Button styling
btn_bg = "#555555"  # Dark grey
btn_fg = "#FFFFFF"  # White
btn_active_bg = "#444444"
btn_font = ('Century Gothic', 15)

back = tk.Button(EmpPage, text="Back", command=lambda: show_frame(MainPage), fg=btn_fg, bg=btn_bg, width=20, height=1, activebackground=btn_active_bg, font=btn_font)
back.place(x=200, y=680)
###################################################################################################

message = tk.Label(Viewframe, text="Attendance For the Date: " + date  ,bg="#D0D3D4" ,fg="black"  ,width=39 ,height=1,font=('Century Gothic', 15, ))
message.place(x=20, y=40)

datef = tk.Label(ViewPage, text =""+day+"-"+mont[month]+"-"+year+"", fg="white",bg="#444444" ,height=1,font=('Century Gothic', 25))
datef.pack()
datef.place(x=760,y=390)

back = tk.Button(ViewPage, text="Back", command=lambda: show_frame(MainPage),fg="white"  ,bg="#404040"  ,width=20  ,height=1, activebackground = "white" ,font=('Century Gothic', 15))
back.place(x=185, y=680)

def openattendancefile():
    tv= ttk.Treeview(Viewframe,height =13,columns = ('name','date','time'))
    tv.column('#0',width=82)
    tv.column('name',width=130)
    tv.column('date',width=133)
    tv.column('time',width=133)
    tv.grid(row=2,column=0,padx=(17,0),pady=(150,0),columnspan=4)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME' )
    scroll = ttk.Scrollbar(Viewframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    with open(askopenfilename()) as csvFile1:
        i = 0
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    message = tk.Label(Viewframe, text=csvFile1.name.split("/")[-1], bg="#D0D3D4", fg="black", width=39, height=1,
                       font=('Century Gothic', 15,))
    message.place(x=20, y=40)

open1 = tk.Button(ViewPage, text="View Attendance", command=lambda: openattendancefile(), fg="white", bg="#404040",
                         width=20, height=1, activebackground="white", font=('Century Gothic', 15))
open1.place(x=180, y=240)

################################################ Unregistered Requests PAGE ########################################################################

endPage = tk.Frame(window, width=1366, height=768)
endPage.grid(row=0, column=0, stick='nsew')
background_label = tk.Label(endPage, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
Requestsframe = tk.Frame(endPage, bg="#D0D3D4")
Requestsframe.place(relx=0.05, rely=0.20, relwidth=0.38, relheight=0.60)

title = tk.Label(Requestsframe, text="Unregistered Requests", bg="#D0D3D4", font=('Century Gothic', 20))
title.place(relx=0.15, y=10)  # Adjusted to position more centrally


def view_requests():
    tv = ttk.Treeview(Requestsframe, height=14, columns=('datetime', 'request'))
    tv.column('#0', width=0, stretch=tk.NO)
    tv.column('datetime', width=220)
    tv.column('request', width=320)
    tv.grid(row=2, column=0, padx=(10, 0), pady=(50, 0), columnspan=4)
    tv.heading('datetime', text='Date and Time')
    tv.heading('request', text='Request')

    scroll = ttk.Scrollbar(Requestsframe, orient='vertical', command=tv.yview)
    scroll.grid(row=2, column=4, padx=(0, 10), pady=(50, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)

    with open("unregistered_requests.txt", 'r') as file:
        for line in file:
            parts = line.split(", Request: ")
            datetime = parts[0].replace("Date and Time: ", "")
            request = parts[1].strip()
            tv.insert('', 'end', values=(datetime, request))


view_requests()

view_requests()

datef = tk.Label(endPage, text=""+day+"-"+mont[month]+"-"+year+"", fg="white", bg="#444444", height=1, font=('Century Gothic', 25))
datef.pack()
datef.place(x=760, y=390)

back = tk.Button(endPage, text="Back", command=lambda: show_frame(MainPage), fg="white", bg="#404040", width=20, height=1, activebackground="white", font=('Century Gothic', 15))
back.place(x=185, y=680)


show_frame(Startup)
########################################################################################################################
window.mainloop()