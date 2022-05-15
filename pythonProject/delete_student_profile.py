# Done

from tkinter import *
from tkinter import ttk, messagebox
import pymongo as pm
import mysql.connector
from PIL import Image, ImageTk


class Delete:
    # Definition of Student Management Console
    def __init__(self, root):
        # Calling a pre_defined Function to fetch all the values of classes
        # Root window Properties
        self.root = root
        self.root.geometry("700x600")
        self.root.title("Remove Student - FacI/^O")

        # Data Members for Storing Data
        client = pm.MongoClient("mongodb://localhost/27027")
        self.db = client['Student_Data']
        self.Encoding = self.db['MCA']
        self.classname = StringVar()
        self.studentroll = StringVar()
        self.studentname = StringVar()
        self.mobile = StringVar()
        self.searchableroll = StringVar()
        self.combo_box_value = StringVar()
        self.dataset_dir = "../Assets/Data"

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1000, 150), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image=self.headerImage)
        header_image_label.pack(side="top", fill="x")

        # Header Label
        header_text_label = Label(self.root, text="Update Student Details", bg="white", fg="blue", font="timesnewroman 15 bold")
        header_text_label.pack(side="top", fill="x")

        # Creation of New Label
        sms_main_frame = Frame(self.root, bd=2, relief=RIDGE)
        sms_main_frame.place(x=50, y=200, width=600, height=325)

        selectclass_text_label = Label(sms_main_frame, text="Select Class")
        selectclass_text_label.grid(row=0, column=0, padx=20, pady=10)

        self.class_box = ttk.Combobox(sms_main_frame, width=70, textvariable=self.combo_box_value, state="readonly")
        self.class_box['values'] = ("--Select--")
        self.class_box.current(0)
        self.class_box.grid(row=0, column=1, padx=20, pady=10)
        self.get_full_class_list()

        # Asking for Roll Number
        roll_label = Label(sms_main_frame, text="Roll Number ")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)
        roll = ttk.Entry(sms_main_frame, textvariable=self.searchableroll, width=73)
        roll.grid(row=1, column=1, padx=20, pady=10, sticky=W)

        buttons_frame = LabelFrame(sms_main_frame, text="", bd=0)
        buttons_frame.place(x=30, y=100, width=500, height=70)

        deleteBtn = Button(buttons_frame, text="Remove Student", width=15, fg="white", bg="red", command=self.delete_roll)
        deleteBtn.grid(row=2, column=0, padx=20, pady=10)
        resetBtn = Button(buttons_frame, text="Reset", width=10, fg="white", bg="gray", command=self.reset_values)
        resetBtn.grid(row=2, column=1, padx=20, pady=10)
        exitBtn = Button(buttons_frame, text="Exit", width=10, fg="white", bg="red", command=self.root.destroy)
        exitBtn.grid(row=2, column=2, padx=20, pady=10)

    def reset_values(self):
        self.class_box.set('--Select--')
        self.searchableroll.set('')

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

    def delete_roll(self):
        if self.searchableroll.get() == "" and self.combo_box_value.get() == "--Select--":
            messagebox.showerror("Error", "Please Fill all the Required Fields", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="",
                                               database="face_recognition")
                my_cursor = conn.cursor()

                my_cursor.execute(f"select * from {self.combo_box_value.get().upper()} where roll=%s",
                                  (self.searchableroll.get(),))
                data = my_cursor.fetchall()
                self.studentroll.set(data[0][0])
                self.studentname.set(data[0][1])
                self.mobile.set(data[0][2])
                self.classname.set(data[0][3])

                msg = my_cursor.execute(
                    f"DELETE FROM {self.class_box.get()} WHERE roll=%s", (
                        self.searchableroll.get(),))
                conn.commit()
                conn.close()
                self.Encoding[self.studentroll.get().upper()].drop()
                if msg == None:
                    messagebox.showinfo("Success", "Student havs been Removed", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"{str(e)}", parent=self.root)


if __name__ == '__main__':
    student_window = Tk()
    obj = Delete(student_window)
    student_window.mainloop()