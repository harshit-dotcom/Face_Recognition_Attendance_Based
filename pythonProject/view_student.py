# Done

from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk


class View:
    # Definition of our Student Management Console
    def __init__(self, root):
        # Calling a pre_defined Function to fetch all the values of classes
        # Root window Properties
        self.root = root
        self.root.geometry("700x600")
        self.root.title("View Student - FacI/^O")

        # Data Members for Storing Data
        self.studentname = StringVar()
        self.studentroll = StringVar()
        self.searchableroll = StringVar()
        self.classname = StringVar()
        self.mobile = StringVar()
        self.combo_box_value = StringVar()

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1000, 150), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image=self.headerImage)
        header_image_label.pack(side="top", fill="x")

        # Header Label
        header_text_label = Label(self.root, text="Student Portfolio", bg="white", fg="blue", font="timesnewroman 15 bold")
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

        searchBtn = Button(sms_main_frame, text="Search", width=10, fg="white", bg="green", command=self.search_for_roll)
        searchBtn.grid(row=2, column=0, padx=20, pady=10)
    # Dividing Frames in Multiple Partitions
        # Left Partition
        choose_class = LabelFrame(sms_main_frame, bd=2, relief=RIDGE, text="Student Details")
        choose_class.place(x=10, y=130, width=575, height=175)

    # Student Details for the Selected Class
        student_details = LabelFrame(choose_class, bd=0, relief=RIDGE, text="")
        student_details.place(x=50, y=10, width=500, height=100)

        # Showing Roll Number
        roll_label = Label(student_details, text="Roll Number ")
        roll_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        roll = ttk.Entry(student_details,textvariable=self.studentroll, state="readonly")
        roll.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Showing Name
        Name_label = Label(student_details, text="Name ")
        Name_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        Name = ttk.Entry(student_details,textvariable=self.studentname, state="readonly")
        Name.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Showing Mobile Number
        Phone_label = Label(student_details, text="Mobile ")
        Phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        Phone = ttk.Entry(student_details,textvariable=self.mobile, state="readonly")
        Phone.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Showing Class
        Class_label = Label(student_details, text="Class ")
        Class_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        Class = ttk.Entry(student_details,textvariable=self.classname, state="readonly")
        Class.grid(row=1, column=3, padx=10, pady=10, sticky=W)

    # Creating a New frame for Command Buttons
        left_frame_buttons = LabelFrame(sms_main_frame, bd=0, relief=RIDGE)
        left_frame_buttons.place(x=65, y=250, width=450, height=50)

        # Buttons Creation
        resetBtn = Button(left_frame_buttons, cursor="hand2", text="Reset", width=14, fg="white", bg="gray", command=self.reset_values)
        resetBtn.grid(row=0, column=1, padx=5, pady=10)
        exitBtn = Button(left_frame_buttons, cursor="hand2", text="Exit", width=14, fg="white", bg="red", command=self.root.destroy)
        exitBtn.grid(row=0, column=2, padx=5, pady=10)

    def reset_values(self):
        self.classname.set('')
        self.studentroll.set('')
        self.studentname.set('')
        self.mobile.set('')

    def get_full_class_list(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognition")
        my_cursor = conn.cursor()
        my_cursor.execute(f"show tables")
        data = my_cursor.fetchall()
        if len(data) !=0:
            self.class_box.set('')
        for i in range(len(data)):
            if str(data[i]) not in self.class_box['values']:
                self.class_box['values'] += (data[i],)

    def search_for_roll(self):
        if self.searchableroll.get() == "":
            messagebox.showerror("Error", "Please Fill in the Roll Number", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="",
                                               database="face_recognition")
                my_cursor = conn.cursor()
                my_cursor.execute(f"select * from {self.combo_box_value.get().upper()} where roll=%s",(self.searchableroll.get(),))
                data = my_cursor.fetchall()
                self.studentroll.set(data[0][0])
                self.studentname.set(data[0][1])
                self.mobile.set(data[0][2])
                self.classname.set(data[0][3])
                conn.commit()
                conn.close()

            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    student_window = Tk()
    obj = View(student_window)
    student_window.mainloop()