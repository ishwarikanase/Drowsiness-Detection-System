from tkinter import *
from tkinter import filedialog
import cv2
import dlib
from math import hypot
import time
import webbrowser

cap=cv2.VideoCapture(0)
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def midpoint(p1,p2):
    return int((p1.x+p2.x)/2),int((p1.y+p2.y)/2)
font=cv2.FONT_HERSHEY_SIMPLEX

master = Tk()


def browsFiles():
    master.filename = filedialog.askopenfilename(initialdir=r"C:",title="Select File", filetypes=(("pdf files","*.pdf"),("all files","*.*")))
    open_file()


def open_file():
    webbrowser.open(master.filename)


    def get_bilnking_ratio(eye_points,facial_landmarks):
        left_point = facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y
        right_point = facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
        ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ratio = hor_line_length / ver_line_length
        return ratio

    def alertUser():
        webbrowser.open("ManacheShlok01.mp3")



    startTime = time.time()



    while True:
        _,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=detector(gray)
        for face in faces:
            landmarks=predictor(gray,face)
            left_eye_ratio=get_bilnking_ratio([36,37,38,39,40,41],landmarks)
            right_eye_ratio = get_bilnking_ratio([42,43,44,45,46,47], landmarks)
            bliking_ratio=(left_eye_ratio+right_eye_ratio)/2


            global flag
            if bliking_ratio > 5:

                if flag==0:

                    startTime=time.time()
                    flag=1
                else:
                    if time.time()-startTime>5:
                        alertUser()
            else:
                flag=0

        key=cv2.waitKey(1)
        if key=="27":
            break
    cap.release()

btn = Button ( master, text="Browse", command=browsFiles)
btn.place(x = 50,y = 50)
mainloop()

