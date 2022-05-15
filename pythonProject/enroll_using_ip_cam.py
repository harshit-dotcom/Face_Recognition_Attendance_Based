# Done

import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import face_recognition
import requests
import numpy as np
import imutils
import cv2 as cv
import mysql.connector
import pymongo as pm
from PIL import Image, ImageTk


class Enroll_Using_Exterenal_Camera:
    # Definition of our Student Management Console
    def __init__(self, root):
        # Calling a pre_defined Function to fetch all the values of classes
        # Root window Properties
        self.root = root
        self.root.geometry("700x500")
        self.root.title("Student Enrollment Console - FacI/^O")

        # Data Members for Storing Data
        self.studentname = StringVar()
        self.studentroll = StringVar()
        self.classname = StringVar()
        self.mobile = StringVar()
        self.url = StringVar()
        self.url.set("192.168.43.1:8080")
        # "http://192.168.82.193:8080/shot.jpg"

        # MongoDB connection Code for localhost if required
        client = pm.MongoClient("mongodb://localhost/27027")
        db = client['Student_Data']
        self.Encoding = db['MCA']

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1000, 150), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image=self.headerImage)
        header_image_label.pack(side="top", fill="x")

        # Header Label
        header_text_label = Label(self.root, text="Student Enrollment", bg="white", fg="blue",
                                  font="timesnewroman 15 bold")
        header_text_label.pack(side="top", fill="x")

        # Creation of New Label
        sms_main_frame = tkinter.Canvas(self.root, bd=2)
        sms_main_frame.place(x=50, y=200, width=600, height=275)

        # Dividing Frames in Multiple Partitions
        # Left Partition
        choose_class = LabelFrame(sms_main_frame, bd=2, relief=RIDGE, text="Select Class")
        choose_class.place(x=10, y=10, width=575, height=250)

        # Showing Roll Number
        camera_ip_label = Label(choose_class, text="Enter Camera IP")
        camera_ip_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        ip_url = ttk.Entry(choose_class, width=70, textvariable=self.url)
        ip_url.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Student Details for the Selected Class
        student_details = LabelFrame(choose_class, bd=0, relief=RIDGE, text="Student Details")
        student_details.place(x=10, y=50, width=525, height=100)

        # Showing Roll Number
        roll_label = Label(student_details, text="Roll Number ")
        roll_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        roll = ttk.Entry(student_details, textvariable=self.studentroll)
        roll.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Showing Name
        Name_label = Label(student_details, text="Name ")
        Name_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        Name = ttk.Entry(student_details, textvariable=self.studentname)
        Name.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Showing Mobile Number
        Phone_label = Label(student_details, text="Mobile ")
        Phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        Phone = ttk.Entry(student_details, textvariable=self.mobile)
        Phone.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Showing Class
        Class_label = Label(student_details, text="Class ")
        Class_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        Class = ttk.Entry(student_details, textvariable=self.classname)
        Class.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Creating a New frame for Command Buttons
        left_frame_buttons = LabelFrame(sms_main_frame, bd=0, relief=RIDGE)
        left_frame_buttons.place(x=21, y=200, width=525, height=50)

        # Buttons Creation
        saveBtn = Button(left_frame_buttons, cursor="hand2", text="Add", width=14, fg="white", bg="green",
                         command=self.enroll_student)
        saveBtn.grid(row=0, column=0, padx=5, pady=10)
        resetBtn = Button(left_frame_buttons, cursor="hand2", text="Reset", width=14, fg="white", bg="gray",
                          command=self.reset_values)
        resetBtn.grid(row=0, column=2, padx=5, pady=10)

        EnrollBtn = Button(left_frame_buttons, cursor="hand2", text="Enroll Face", width=14, fg="black",
                           bg="lightgreen", command=self.enroll_face_using_ip_webcam)
        EnrollBtn.grid(row=0, column=1, padx=5, pady=10)
        exitBtn = Button(left_frame_buttons, cursor="hand2", text="Exit", width=14, fg="white", bg="red",
                         command=self.root.destroy)
        exitBtn.grid(row=0, column=3, padx=5, pady=10)

    def enroll_face_using_ip_webcam(self):
        i = 0
        while i < 10:
            video = requests.get(f"http://{self.url.get()}/shot.jpg")
            cimg = np.array(bytearray(video.content), dtype=np.uint8)
            img = cv.imdecode(cimg, -1)
            img = imutils.resize(img, width=600, height=600)
            face = face_recognition.face_locations(img)
            encoding = face_recognition.face_encodings(img, face)
            for f, e in zip(face, encoding):
                if len(face) == 1:
                    self.draw_rectangle_white(img, f)
                    self.Encoding[self.studentroll.get().upper()].insert_one(
                        {"Name": str(self.studentname.get().upper()),
                         'mobile': self.mobile.get().upper(),
                         "Rollno": self.studentroll.get().upper(), "Enc": e.tolist()})
                    cv.putText(img, str((i + 1) * 2) + " %", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                               1)
                    i += 1
            if cv.waitKey(1) == ord('q'):
                break
            cv.imshow("Face Training", img)
        cv.destroyAllWindows()

    def enroll_student(self):
        if self.studentname.get() == "" or self.studentroll.get() == "" or self.mobile.get() == "" or self.classname.get() == "":
            messagebox.showerror("Error", "Please Fill all the Required Fields", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="",
                                               database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute(f"create table if not exists {self.classname.get().upper()} ("
                                  f"roll varchar(30) primary key,"
                                  f"name varchar(50),"
                                  f"mobile varchar(15),"
                                  f"class varchar(50));")
                msg = my_cursor.execute(f"insert into {self.classname.get().upper()} values ("
                                        f"%s,%s,%s,%s)", (
                                            self.studentroll.get(),
                                            self.studentname.get().upper(),
                                            self.mobile.get(),
                                            self.classname.get().upper()))
                conn.commit()
                conn.close()
                if msg == None:
                    messagebox.showinfo("Success", "Details have been saved", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"{str(e)}", parent=self.root)

    def reset_values(self):
        self.classname.set('')
        self.studentroll.set('')
        self.studentname.set('')
        self.mobile.set('')


    # Draw a Rectangle on Detected face of red Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_red(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (0, 0, 255), 2)

    # Draw a Rectangle on Detected face of Green Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_green(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (0, 255, 0), 2)

    # Draw a Rectangle on Detected face of White Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_white(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (255, 255, 255), 2)


if __name__ == '__main__':
    student_window = Tk()
    obj = Enroll_Using_Exterenal_Camera(student_window)
    student_window.mainloop()
