import cv2 as cv
import mysql.connector
import time
import numpy as np
import face_recognition
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
import pymongo as pm


class Mark_Attendance:
    def __init__(self, root):
        # Structure of the root Window
        self.root = root
        self.root.geometry("500x300")
        self.root.title("Facial Attendance System - FacI/^O")

        # Creation of a frame inside the root window
        sms_left_frame = Frame(self.root, bd=2, relief=RIDGE)
        sms_left_frame.place(x=10, y=10, width=400, height=250)

        # Variables that are to be used by the whole instance
        # MongoDB connection Code for localhost if required
        client = pm.MongoClient("mongodb://localhost/27027")
        self.db = client['Student_Data']
        self.attendb = client['Attendences']
        self.Encoding = self.db['MCA']
        self.attendance_duration = StringVar()
        self.combo_box_value = StringVar()
        self.lecture_name = StringVar()

        # Defining structure of the ComboBox and Button in the Root
        box_label = Label(sms_left_frame, width=20, text="Select Class ")
        box_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.class_box = ttk.Combobox(sms_left_frame, width=20, textvariable=self.combo_box_value, state="readonly")
        self.class_box['values'] = ("--Select--")
        self.class_box.current(0)
        self.class_box.grid(row=0, column=1, padx=20, pady=10)
        self.get_full_class_list()

        # Getting the Lecture Name
        name_label = Label(sms_left_frame, width=20, text="Lecture Name ")
        name_label.grid(row=1, column=0, padx=15, pady=10, sticky=W)
        Lname = ttk.Entry(sms_left_frame, textvariable=self.lecture_name)
        Lname.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Getting the Attendance Duration
        Phone_label = Label(sms_left_frame, width=20, text="Lecture Duration ")
        Phone_label.grid(row=2, column=0, padx=15, pady=10, sticky=W)
        Phone = ttk.Entry(sms_left_frame, textvariable=self.attendance_duration)
        Phone.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Deploying the Camera using Button Command
        EnrollBtn = Button(sms_left_frame, cursor="hand2", text="Launch Camera", width=14, fg="white", bg="green",
                           command=self.mark_attendace)
        EnrollBtn.grid(row=3, column=0, padx=10, pady=10)

        ExitBtn = Button(sms_left_frame, cursor="hand2", text="Close", width=14, fg="white", bg="red",
                         command=self.root.destroy)
        ExitBtn.grid(row=3, column=1, padx=10, pady=10)

    def mark_attendace(self):
        classname = self.class_box.get()
        present_list = self.RecognizeusingBuiltinWebcam(self.attendance_duration.get())
        marked = []
        for person in present_list:
            if person not in marked:
                newdict = {"Person": person, "Lecture Name:": classname.upper(),
                           "Date & Time": datetime.now()}
                self.attendb[self.class_box.get().upper()].insert_one(newdict)
                marked.append(person)

    def get_full_class_list(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute(f"show tables")
        data = my_cursor.fetchall()
        if len(data) != 0:
            self.class_box.set('')
        for i in range(len(data)):
            if str(data[i]) not in self.class_box['values']:
                self.class_box['values'] += (data[i],)

    # Recognising Persons and Returning Every Iteration persons to a list
    def RecognizeusingBuiltinWebcam(self, total_time):
        try:
            total_encodings = self.fetch_encodings_from_db()
            known_encodings = [person['Enc'] for person in total_encodings]
            present_persons = []
            video = cv.VideoCapture(0)
            end = time.time() + float(total_time) * 60
            while time.time() < end:
                __, img = video.read()
                cimg = cv.resize(img, (0, 0), None, 0.25, 0.25)
                face = face_recognition.face_locations(cimg)
                test_image_encoding = face_recognition.face_encodings(cimg, face)
                for f, e in zip(face, test_image_encoding):
                    if len(known_encodings) > 0:
                        is_a_match = face_recognition.compare_faces(known_encodings, e, 0.5)
                        face_distance = face_recognition.face_distance(known_encodings, e)
                        best_match = np.argmin(face_distance)
                        if is_a_match and face_distance[best_match] < 0.45:
                            person = total_encodings[best_match]
                            if {"Name": person['Name'], "Rollno": person['Rollno']} not in present_persons:
                                present_persons.append({"Name": person['Name'], "Rollno": person['Rollno']})
                            # for encoding in total_encodings:
                            #     if encoding['Rollno'] == person['Rollno']:
                            #         total_encodings.remove(encoding)
                            #         known_encodings.remove(encoding['Enc'])
                    else:
                        cv.destroyAllWindows()
                        video.release()
                        messagebox.showinfo("Success", "Attendence has been marked")
                        return present_persons
                if cv.waitKey(5) == ord('q'):
                    cv.destroyAllWindows()
                    break
            video.release()
            cv.destroyAllWindows()
            messagebox.showinfo("Success", "Attendence has been marked")
            return present_persons
        except Exception as e:
            messagebox.showerror("An error Occurred", str(e))

    # Check how many persons are Enrolled in the Class
    # Returns List of Dictionaries
    def fetch_encodings_from_db(self):
        found_Encodings = []
        class_list = self.db.list_collection_names()
        for i in range(len(class_list)):
            current_person = self.db[class_list[i]]
            docs = current_person.find({}, {'_id': 0})
            for doc in docs:
                found_Encodings.append(doc)
        return found_Encodings

    # Draw a Rectangle on Detected face of red Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_red(self, img, c):
        x, y, w, h = c
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Draw a Rectangle on Detected face of Green Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_green(self, img, c):
        x, y, w, h = c
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Draw a Rectangle on Detected face of White Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_white(self, img, c):
        x, y, w, h = c
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)


if __name__ == '__main__':
    root = Tk()
    obj = Mark_Attendance(root)
    root.mainloop()
