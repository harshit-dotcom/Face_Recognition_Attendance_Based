import cv2 as cv

class Detect_Persons:
    def __init__(self):
        self.haar_face_cascade = cv.CascadeClassifier("Data/Assets/frontal_faces/haarcascade_frontalface_default.xml")


    # Detecting Multiple Persons
    def Detect(self):
        video = cv.VideoCapture(0)
        while True:
            __, img = video.read()
            face = self.haar_face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
            for f in face:
                self.draw_rectangle_white(img, f)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
            cv.imshow("Face Detection", img)
        video.release()
        cv.destroyAllWindows()

    # Draws a Rectangle on Detected face of White Color using face co-ordinated using cv.rectangle()
    def draw_rectangle_white(self, img, c):
        x, y, w, h = c
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

if __name__ == '__main__':
    obj = Detect_Persons()
    obj.Detect()