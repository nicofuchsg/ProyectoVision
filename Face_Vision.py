import numpy as np
import cv2
import matplotlib.pyplot as plt
import Datos_util
import time

TEST_FLAG = 100

face_cascades_list = []

#face_cascades_list.append('haarcascade_face.xml')
face_cascades_list.append('CUDAcascade_face.xml')
face_cascades_list.append('LBPcascade_face.xml')
face_cascades_list.append('CUDAcascade_face_2.xml')
face_cascades_list.append('CUDAcascade_face_3.xml')
#face_cascades_list.append('cascade_MIO.xml') #--> MALO
#face_cascades_list.append('haarcascade_face_2.xml')

#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eye_cascade = cv2.CascadeClassifier('CUDAcascade_eye2.xml')

datos_totales = []

for cascade in face_cascades_list:
    tiempo_inicial = time.time()
    cap = cv2.VideoCapture("Teaching_1st_Graders.mp4")
    #Ancho 1280
    cap.set(4,720)
    #Largo 720
    cap.set(5,680)
    # FPS
    cap.set(6,10)

    face_cascade = cv2.CascadeClassifier(cascade)
    
    datos_informe = []

    testing = 0

    while (cap.isOpened()):
        testing += 1
        if testing > TEST_FLAG:
            break
        ret, img = cap.read()
        #Para eficiencia
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #caras dentro del clasificador
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        contador = 0
        for (x,y,w,h) in faces:
            contador += 1
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #Guardamos contador para analizar despues
        datos_informe.append(contador)
        #Agregamos numero de niños
        font = cv2.FONT_HERSHEY_TRIPLEX
        thickness = 2
        texto_caras = "Caras: " + str(contador)
        posicion = (20,40)
        color_texto = 255
        cv2.putText(img,texto_caras, posicion, font,thickness, color_texto)
        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    #print("-"*20)
    promedio = Datos_util.promedio(datos_informe)
    tiempo_ejecucion = time.time() - tiempo_inicial
    datos_totales.append([cascade,promedio,tiempo_ejecucion])
    #print("Tiempo de ejecucion", tiempo_ejecucion)
    #print("-"*20)

    #Ploteo Informe
    plt.plot(datos_informe, label=cascade)
plt.title("Clasificadores")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,  ncol=2, mode="expand", borderaxespad=0.)
plt.show()

for data in datos_totales:
    plt.plot(data[1],data[2],'o',label=data[0])

plt.title("Time vs FaceDetec")
plt.xlabel('Face Number')
plt.ylabel('Time')
plt.legend()
plt.show()