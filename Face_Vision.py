import numpy as np
import cv2
import matplotlib.pyplot as plt
import Datos_util
import time

TEST_FLAG = 600

face_cascades_list = []

##--> estos son los algoritmos de aprendizaje y reconocimiento de caras <--##

face_cascades_list.append('haarcascade_face.xml')
#face_cascades_list.append('CUDAcascade_face.xml')
#face_cascades_list.append('LBPcascade_face.xml')
#face_cascades_list.append('CUDAcascade_face_2.xml')
#face_cascades_list.append('CUDAcascade_face_3.xml')
#face_cascades_list.append('cascade_MIO.xml') #--> MALO
#face_cascades_list.append('haarcascade_face_2.xml')


##--> estos son los algoritmos de aprendizaje y reconocimiento de ojos <--##

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#eye_cascade = cv2.CascadeClassifier('CUDAcascade_eye2.xml')

datos_totales = []

#cascade es cada uno de los algoritmos agregados a la lista face_cascades_list
for cascade in face_cascades_list:

    ##--> en toda esta parte solo se dan caracteristicas de como va a ser el video <--##

    #para el inicio del algoritmo anotar el tiempo en que inicia
    tiempo_inicial = int(time.time())
    #lee archivos de video
    cap = cv2.VideoCapture("ezgif.com-cut-video.mp4")
    #Ancho 1280 , se agrega una propiedad en el videocapture
    cap.set(4,720)
    #Largo 720, se agrega una propiedad en el videocapture
    cap.set(5,680)
    # FPS, se agregan los frames per second
    cap.set(6,10)

    #nombre del clasificador que vamos a usar en esta iteracion
    face_cascade = cv2.CascadeClassifier(cascade)
    
    datos_informe = []

    testing = 0

    #mientras el video este abierto
    while (cap.isOpened()):
        tiempo_actual = int(time.time())
        diferencia_tiempo = tiempo_actual-tiempo_inicial
        testing += 1
        #se hace un test con los primeros 100 flags del video
        if testing > TEST_FLAG:
            break
        #imagen del video y ret?
        ret, img = cap.read()
        if diferencia_tiempo % 2 == 0 or diferencia_tiempo == 0:
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
            #Agregamos numero de ninios
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
