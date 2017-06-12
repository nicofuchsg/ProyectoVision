import numpy as np
import cv2
import time


#face_cascade = cv2.CascadeClassifier('haarcascade_face.xml')
face_cascade = cv2.CascadeClassifier('CUDAcascade_face.xml')
#face_cascade = cv2.CascadeClassifier('CUDAcascade_face_2.xml')
#face_cascade = cv2.CascadeClassifier('CUDAcascade_face_3.xml')
#face_cascade = cv2.CascadeClassifier('CUDAcascade_face_alt_tree.xml')

#face_cascade = cv2.CascadeClassifier('haarcascade_face_MIO.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eye_cascade = cv2.CascadeClassifier('CUDAcascade_eye2.xml')


cap = cv2.VideoCapture("Teaching_1st_Graders.mp4")
#Ancho 1280
cap.set(4,720)
#Largo 720
cap.set(5,680)
# FPS
cap.set(6,10)

while (cap.isOpened()):
    #time.sleep(2)
    ret, img = cap.read()
    #Para eficiencia
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #caras dentro del clasificador
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()