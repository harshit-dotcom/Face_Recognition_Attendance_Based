# Done

import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import face_recognition
import cv2 as cv
import pymongo as pm


class SMS:
    # Definition of our Student Management Console
    def __init__(self, root):
        # Calling a pre_defined Function to fetch all the values of classes
        # Root window Properties
        self.root = root
        self.root.geometry("1500x1000")
        self.root.title("Student Management System - FacI/^O")

        # MongoDB connection Code for localhost if required
        client = pm.MongoClient("mongodb://localhost/27027")
        db = client['Student_Data']
        self.Encoding = db['MCA']

        # Data Members for Storing Data
        self.studentname = StringVar()
        self.studentroll = StringVar()
        self.classname = StringVar()
        self.mobile = StringVar()
        self.combo_box_value = StringVar()

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1500, 200), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image=self.headerImage)
        header_image_label.pack(side="top", fill="x")

        # Header Label
        header_text_label = Label(self.root, text="Student Management System - Fac^I/O", bg="white", fg="blue",
                                  font="timesnewroman 20 bold")
        header_text_label.pack(side="top", fill="x")

        # Background Image
        bgimg = Image.open("Data/Assets/face_header_sd.jpg")
        bgimg = bgimg.resize((1500, 600), Image.ANTIALIAS)
        self.bgImage = ImageTk.PhotoImage(bgimg)

        # Background Image is Packed
        background_image_label = Label(self.root, image=self.bgImage)
        background_image_label.pack(side="top", fill="x")

        # Creation of New Label
        sms_main_frame = tkinter.Canvas(self.root, bd=2, scrollregion=(0, 0, 1450, 600))
        sms_main_frame.place(x=20, y=260, width=1450, height=600)

        # Creating a Scroll bar
        scroll_x_main = Scrollbar(sms_main_frame, orient=HORIZONTAL)
        sms_main_frame['xscrollcommand'] = scroll_x_main.set
        scroll_x_main.pack(side="bottom", fill="x")
        scroll_x_main.config(command=sms_main_frame.xview)

    # Dividing Frames in Multiple Partitions
        # Left Partition
        sms_left_frame = LabelFrame(sms_main_frame, bd=2, relief=RIDGE, text="Details")
        sms_left_frame.place(x=10, y=10, width=550, height=550)

        choose_class = LabelFrame(sms_left_frame, bd=2, relief=RIDGE, text="Select Class")
        choose_class.place(x=10, y=10, width=520, height=500)

        self.class_box = ttk.Combobox(choose_class, width=70, textvariable= self.combo_box_value, state="readonly")
        self.class_box['values'] = ("--Select--")
        self.class_box.current(0)
        self.class_box.grid(row=0, column=1, padx=20, pady=10)
        self.get_full_class_list()

        searchclassesBtn = Button(choose_class, text="->", cursor="hand2", width=5 , fg="white", bg="green", command=self.fetch_data)
        searchclassesBtn.grid(row=0, column=2, padx=5, pady=10)

    # Student Details for the Selected Class
        student_details = LabelFrame(choose_class, bd=2, relief=RIDGE, text="Student Details")
        student_details.place(x=20, y=50, width=480, height=150)

        # Showing Roll Number
        roll_label = Label(student_details, text="Roll Number ")
        roll_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        roll = ttk.Entry(student_details,textvariable=self.studentroll)
        roll.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Showing Name
        Name_label = Label(student_details, text="Name ")
        Name_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        Name = ttk.Entry(student_details,textvariable=self.studentname)
        Name.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Showing Mobile Number
        Phone_label = Label(student_details, text="Mobile ")
        Phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        Phone = ttk.Entry(student_details,textvariable=self.mobile)
        Phone.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Showing Class
        Class_label = Label(student_details, text="Class ")
        Class_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        Class = ttk.Entry(student_details,textvariable=self.classname)
        Class.grid(row=1, column=3, padx=10, pady=10, sticky=W)

    # Creating a New frame for Command Buttons
        left_frame_buttons = LabelFrame(sms_left_frame, bd=2, relief=RIDGE)
        left_frame_buttons.place(x=31, y=250, width=480, height=150)

        # Buttons Creation
        saveBtn = Button(left_frame_buttons, cursor="hand2", text="Enroll", width=14, fg="white", bg="green", command=self.enroll_student)
        saveBtn.grid(row=0, column=0, padx=5, pady=10)
        updateBtn = Button(left_frame_buttons, cursor="hand2", text="Update", width=14, fg="white", bg="green", command=self.update_student_data)
        updateBtn.grid(row=0, column=1, padx=5, pady=10)
        resetBtn = Button(left_frame_buttons, cursor="hand2", text="Reset", width=14, fg="white", bg="gray", command=self.reset_values)
        resetBtn.grid(row=0, column=2, padx=5, pady=10)
        deleteBtn = Button(left_frame_buttons, cursor="hand2", text="Delete", width=14, fg="white", bg="red", command=self.delete_student_data)
        deleteBtn.grid(row=0, column=3, padx=5, pady=10)

        UpdateFace = Button(left_frame_buttons, cursor="hand2", text="Update Face", width=14, fg="white", bg="yellow")
        UpdateFace.grid(row=1, column=1, padx=5, pady=10)
        exitBtn = Button(left_frame_buttons, cursor="hand2", text="Exit", width=14, fg="white", bg="red", command=self.root.destroy)
        exitBtn.grid(row=1, column=2, padx=5, pady=10)

        # Right Partition
        sms_right_frame = LabelFrame(sms_main_frame, bd=2, relief=RIDGE, text="Class List")
        sms_right_frame.place(x=600, y=10, width=800, height=550)

        # Student Table in which all students will be shown
        studentframe = LabelFrame(sms_right_frame, bd=2, relief=RIDGE, text="Student List")
        studentframe.place(x=10, y=10, width=780, height=500)
        scroll_x_students = Scrollbar(studentframe, orient=HORIZONTAL)
        scroll_y_students = Scrollbar(studentframe, orient=VERTICAL)

        self.studentTable = ttk.Treeview(studentframe, column=("Roll Number", "Name", "Mobile", "Class"), xscrollcommand=scroll_x_students.set, yscrollcommand=scroll_y_students.set)

        scroll_x_students.pack(side=BOTTOM, fill="x")
        scroll_y_students.pack(side=RIGHT, fill="y")

        self.studentTable.heading("Roll Number", text="Roll")
        self.studentTable.heading("Name", text="Name")
        self.studentTable.heading("Mobile", text="Mobile Number")
        self.studentTable.heading("Class", text="Class")
        self.studentTable['show'] = "headings"
        self.studentTable.pack(fill=BOTH, expand=1)
        self.studentTable.bind("<ButtonRelease>", self.get_values_from_student_list)

        scroll_x_students.config(command=self.studentTable.xview)
        scroll_y_students.config(command=self.studentTable.yview)

    # Registering a new Person's face
    def enroll_student(self):
        if self.studentname.get() == "" or self.studentroll.get() == "" or self.mobile.get() == "" or self.classname.get() == "":
            messagebox.showerror("Error", "Please Fill all the Required Fields", parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute(f"create table if not exists {self.classname.get().upper()} ("
                                  f"roll varchar(30) primary key,"
                                  f"name varchar(50),"
                                  f"mobile varchar(15),"
                                  f"class varchar(50));")
                msg = my_cursor.execute(f"insert into {self.classname.get().upper()} values ("
                                        f"%s,%s,%s,%s)",(
                                            self.studentroll.get(),
                                            self.studentname.get().upper(),
                                            self.mobile.get(),
                                            self.classname.get().upper()))
                conn.commit()
                conn.close()
                try:
                    video = cv.VideoCapture(0)
                    i = 0
                    while i < 10:
                        _, cimg = video.read()
                        face = face_recognition.face_locations(cimg)
                        encoding = face_recognition.face_encodings(cimg, face)
                        for f, e in zip(face, encoding):
                            if len(face) == 1:
                                self.draw_rectangle_white(cimg, f)
                                self.Encoding[self.studentroll.get().upper()].insert_one(
                                    {"Name": str(self.studentname.get().upper()),
                                     'mobile': self.mobile.get().upper(),
                                     "Rollno": self.studentroll.get().upper(), "Enc": e.tolist()})
                                cv.putText(cimg, str((i + 1) * 3.33) + " %", (10, 30), cv.FONT_HERSHEY_COMPLEX, 1,
                                           (255, 255, 255),
                                           1)
                                i += 1
                        if cv.waitKey(1) == ord('q'):
                            break
                        cv.imshow("Face Enrollment Window", cimg)
                    video.release()
                    cv.destroyAllWindows()
                    messagebox.showinfo("Success", "Details have been saved", parent=self.root)
                    self.root.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Student Alredy Registered with Roll: {self.studentroll.get()}", parent=self.root)

    def get_full_class_list(self):
        conn = mysql.connector.connect(host="localhost", user="root",  password="", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute(f"show tables")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.class_box.set('')
        for i in range(len(data)):
            if str(data[i]) not in self.class_box['values']:
                self.class_box['values'] += (data[i],)
        conn.commit()
        conn.close()


    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute(f"select * from {self.class_box.get().upper()}")
        data=my_cursor.fetchall()
        self.studentTable.delete(*self.studentTable.get_children())
        if len(data)!=0:
            for dataitem in data:
                self. studentTable.insert('',END, values=dataitem)
            conn.commit()
        conn.close()


    def get_values_from_student_list(self, event=''):
        focus = self.studentTable.focus()
        item = self.studentTable.item(focus)
        data = item['values']
        self.studentroll.set(data[0])
        self.studentname.set(data[1])
        self.mobile.set(data[2])
        self.classname.set(data[3])



    def update_student_data(self):
        if self.studentname.get() == "" or self.studentroll.get() == "" or self.mobile.get() == "" or self.classname.get() == "":
            messagebox.showerror("Error", "Please Fill all the Required Fields", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute(f"update {self.classname.get().upper()} set roll=%s, name=%s, mobile=%s, class=%s where roll= %s",(
                                        self.studentroll.get(),
                                        self.studentname.get(),
                                        self.mobile.get(),
                                        self.classname.get(),
                                        self.studentroll.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Details have been Updated", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"{str(e)}", parent=self.root)

    def delete_student_data(self):
        if self.studentroll.get() == "":
            messagebox.showerror("Error", "Please Fill all the Required Fields", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="",
                                               database="face_recognition")
                my_cursor = conn.cursor()
                msg = my_cursor.execute(
                    f"DELETE FROM {self.class_box.get()} WHERE roll=%s", (
                        self.studentroll.get(),))
                conn.commit()
                conn.close()
                if msg == None:
                    messagebox.showinfo("Success", "Student Details have been Removed", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"{str(e)}", parent=self.root)

    def reset_values(self):
        self.class_box.set('')
        self.studentTable.delete(*self.studentTable.get_children())
        self.classname.set('')
        self.studentroll.set('')
        self.studentname.set('')
        self.mobile.set('')

    # Draw a Rectangle on Detected face of White Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_white(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (255, 255, 255), 2)

if __name__ == '__main__':
    student_window = Tk()
    obj = SMS(student_window)
    student_window.mainloop()