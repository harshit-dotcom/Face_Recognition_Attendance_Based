
from tkinter import *
from PIL import Image, ImageTk
from sms import SMS
from Recognize_persons import Recognize_Persons
from Mark_Attendance import Mark_Attendance
from detectfaceonly import Detect_Persons
from enroll_new_student import Enroll
from update_student_profile import Update
from delete_student_profile import Delete
from view_student import View
from enroll_using_ip_cam import Enroll_Using_Exterenal_Camera
from recognize_using_ip_webcam import Recognize_Persons_Using_IP_Webcam

class Face_Recognition:
    # Definition of our Main/ Root window
    def __init__(self, root):
        # Root window Properties
        self.root = root
        self.root.geometry("1500x1000")
        self.root.title("FacI/^O")

        # Header Label
        header_text_label = Label(self.root, text="Welcome to Fac^I/O", bg="white", fg="blue",
                                  font="timesnewroman 20 bold")
        header_text_label.pack(side="top", fill="x")

        # Header Image
        img = Image.open("Data/Assets/face_header_sd.jpg")
        img = img.resize((1500, 650), Image.ANTIALIAS)
        self.headerImage = ImageTk.PhotoImage(img)

        # Header Image is Shown
        header_image_label = Label(self.root, image = self.headerImage)
        header_image_label.pack(side="bottom", fill="x")

    # Creating a Menu bar
        menubar = Menu(self.root)

        # View Section
        file = Menu(menubar, tearoff=0)
        file.add_command(label="Student List", command=self.students)
        file.add_command(label="View Profile", command=self.view_student)
        menubar.add_cascade(label="View", menu=file)

        # Edit Section
        view = Menu(menubar, tearoff=0)
        view.add_command(label="Update Profile", command=self.update)
        view.add_command(label="Update Roll Number")
        view.add_command(label = "Update Face")
        view.add_separator()
        view.add_command(label="Delete Profile", command=self.Delete)
        menubar.add_cascade(label="Edit", menu=view)

        # Utilities Section
        tools = Menu(menubar, tearoff=0)
        tools.add_command(label="Enroll", command = self.enroll)
        tools.add_command(label="Enroll using IP Camera", command = self.Enroll_using_IP_Webcam)
        tools.add_command(label="Detect Face", command=self.detect)
        tools.add_command(label="Recognise Person", command=self.recognize)
        tools.add_command(label="Recognise Person using IP camera", command=self.Recognise_using_ip_webcam)
        tools.add_command(label="Mark Attendance", command=self.attendace)
        tools.add_separator()
        menubar.add_cascade(label="Utilities", menu=tools)

        # Exit Button
        menubar.add_cascade(label="Exit", command=self.root.destroy)

        # Configuring the Menu Bar
        self.root.config(menu=menubar)

    def recognize(self):
        self.recognizeobj = Recognize_Persons()
        self.recognizeobj.Recognize()

    def students(self):
        self.new_window = Toplevel(self.root)
        self.app = SMS(self.new_window)

    def attendace(self):
        self.a_window = Toplevel(self.root)
        self.attendanceobj = Mark_Attendance(self.a_window)

    def detect(self):
        self.detectobj = Detect_Persons()
        self.detectobj.Detect()

    def enroll(self):
        self.enroll_window = Toplevel(self.root)
        self.enroll_app = Enroll(self.enroll_window)

    def update(self):
        self.update_window = Toplevel(self.root)
        self.update_app = Update(self.update_window)

    def Delete(self):
        self.delete_obj = Toplevel(self.root)
        self.delete_app = Delete(self.delete_obj)

    def view_student(self):
        self.view_obj = Toplevel(self.root)
        self.view_app = View(self.view_obj)

    def Enroll_using_IP_Webcam(self):
        self.enrollip_obj = Toplevel(self.root)
        self.enroll_app = Enroll_Using_Exterenal_Camera(self.enrollip_obj)

    def Recognise_using_ip_webcam(self):
        self.recg_obj = Toplevel(self.root)
        self.recg_app = Recognize_Persons_Using_IP_Webcam(self.recg_obj)


if __name__ == '__main__':
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
