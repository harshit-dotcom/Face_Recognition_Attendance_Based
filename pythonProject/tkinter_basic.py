# Done
import cv2 as cv
import pymongo as pm
import numpy as np
import face_recognition
import multiprocessing


class Recognize_Persons:
    def __init__(self):
        # MongoDB connection Code for localhost if required
        client = pm.MongoClient("mongodb://localhost/27027")
        self.db = client['Student_Data']
        self.Encoding = self.db['MCA']
        self.matched_index = 0

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

    # # Using Multiprocessing to enchance the speed
    # def process(self):
    #     multiprocessing.Process(target=self.Recognize(), args=(self,))

    def show_results(self, f, e, known_encodings):
            is_a_match = face_recognition.compare_faces(known_encodings, e)
            face_distance = face_recognition.face_distance(known_encodings, e)
            best_match = np.argmin(face_distance)
            if is_a_match and face_distance[best_match] < 0.48:
                self.matched_index = best_match
            else:
                self.matched_index = None

    # Recognising Persons and Returning Every Iteration persons to a list
    def Recognize(self):
        total_encodings = self.fetch_encodings_from_db()
        known_encodings = np.array([d['Enc'] for d in total_encodings])
        present_persons = []
        video = cv.VideoCapture(0)
        while True:
            __, img = video.read()
            cimg = cv.resize(img, (0, 0), None, 0.25, 0.25)
            face = face_recognition.face_locations(cimg)
            test_image_encoding = face_recognition.face_encodings(cimg, face)
            for f, e in zip(face, test_image_encoding):
                p = multiprocessing.Process(target=self.show_results(f, e, known_encodings), args=(f, e))
                p.start()
                p.join()
                if self.matched_index is not None:
                    person = total_encodings[self.matched_index]
                    print(person)
                    self.draw_rectangle_green(img, [f[0] * 4, f[1] * 4, f[2] * 4, f[3] * 4])
                    cv.putText(img, person['Name'], (f[3] * 4, f[0] * 4 - 4), cv.FONT_HERSHEY_PLAIN, 0.8,
                               (255, 255, 255))
                    if {"Name": person['Name'], "Rollno": person['Rollno']} not in present_persons:
                        present_persons.append({"Name": person['Name'], "Rollno": person['Rollno']})
                else:
                    person = "Unknown"
                    self.draw_rectangle_red(img, [f[0] * 4, f[1] * 4, f[2] * 4, f[3] * 4])
                    cv.putText(img, person, (f[3] * 4, f[0] * 4 - 4), cv.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
            cv.imshow("Face Recognition", img)
        video.release()
        cv.destroyAllWindows()

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
    obj = Recognize_Persons()
    obj.Recognize()