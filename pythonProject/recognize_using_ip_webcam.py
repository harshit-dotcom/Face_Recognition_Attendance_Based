# Done



import cv2 as cv
import requests
import numpy as np
import tkinter
import imutils
from tkinter import *
import pymongo as pm
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import face_recognition


class Recognize_Persons_Using_IP_Webcam:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x500")
        self.root.title("Student Recognition System - FacI/^O")

        self.url = StringVar()
        self.url.set("192.168.43.1:8080")

        # MongoDB connection Code for localhost if required
        client = pm.MongoClient("mongodb://localhost/27027")
        self.db = client['Student_Data']
        self.Encoding = self.db['MCA']

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1000, 150), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image=self.headerImage)
        header_image_label.pack(side="top", fill="x")

        # Header Label
        header_text_label = Label(self.root, text="Student Recognition", bg="white", fg="blue",
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

        left_frame_buttons = LabelFrame(sms_main_frame, bd=0, relief=RIDGE)
        left_frame_buttons.place(x=21, y=100, width=525, height=50)

        # Buttons Creation
        saveBtn = Button(left_frame_buttons, cursor="hand2", text="Add", width=14, fg="white", bg="green",
                         command=self.Recognize)
        saveBtn.grid(row=0, column=0, padx=5, pady=10)

    # Recognising Persons and Returning Every Iteration persons to a list
    def Recognize(self):
        total_encodings = self.fetch_encodings_from_db()
        known_encodings = np.array([d['Enc'] for d in total_encodings])
        present_persons = []
        while True:
            try:
                video = requests.get(f"http://{self.url.get()}/shot.jpg")
                cimg = np.array(bytearray(video.content), dtype=np.uint8)
                timg = cv.imdecode(cimg, -1)
                timg = imutils.resize(timg, width=600, height=600)
                img = cv.resize(timg, (0, 0), None, 0.25, 0.25)
                face = face_recognition.face_locations(img)
                test_image_encoding = face_recognition.face_encodings(img, face)
                for f, e in zip(face, test_image_encoding):
                    is_a_match = face_recognition.compare_faces(known_encodings, e, 0.5)
                    face_distance = face_recognition.face_distance(known_encodings, e)
                    best_match = np.argmin(face_distance)
                    if is_a_match and face_distance[best_match] < 0.50:
                        person = total_encodings[best_match]
                        self.draw_rectangle_green(timg, [f[0] * 4, f[1] * 4, f[2] * 4, f[3] * 4])
                        cv.putText(timg, person['Name'], (f[3] * 4, f[0] * 4 - 4), cv.FONT_HERSHEY_PLAIN, 0.8,
                                   (255, 255, 255))
                        if {"Name": person['Name'], "Rollno": person['Rollno']} not in present_persons:
                            present_persons.append({"Name": person['Name'], "Rollno": person['Rollno']})
                    else:
                        person = "Unknown"
                        self.draw_rectangle_red(timg, [f[0] * 4, f[1] * 4, f[2] * 4, f[3] * 4])
                        cv.putText(timg, person, (f[3] * 4, f[0] * 4 - 4), cv.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))
                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    break
                cv.imshow("Face Recognition", timg)
            except Exception as e:
                pass
        cv.destroyAllWindows()

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

    # Draws a Rectangle on Detected face of red Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_red(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (0, 0, 255), 2)

    # Draws a Rectangle on Detected face of Green Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_green(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (0, 255, 0), 2)

    # Draws a Rectangle on Detected face of White Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_white(self, img, c):
        t, r, b, l = c
        cv.rectangle(img, (l, t), (r, b), (255, 255, 255), 2)


if __name__ == '__main__':
    my_obj = Tk()
    obj = Recognize_Persons_Using_IP_Webcam(my_obj)
    my_obj.mainloop()
