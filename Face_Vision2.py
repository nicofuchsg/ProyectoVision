import numpy as np
import cv2
import face_recognition
import matplotlib.pyplot as plt
import Datos_util
import time
import data_excel

TEST_FLAG = 100

datos_totales = []
datos_informe = []
testing = 0
excel_data = data_excel.DataExcel()
tiempo_inicial = time.time()


#para el inicio del algoritmo anotar el tiempo en que inicia
tiempo_inicial = int(time.time())
#lee archivos de video
#cap = cv2.VideoCapture("Whole_Brain_Teaching__Grade_1_Classroom.mp4")
cap = cv2.VideoCapture("Teaching_1st_Graders.mp4")

# Load sample picture and learn how to recognize it.
profesor_image = face_recognition.load_image_file("profesora.png")
#profesor_image = face_recognition.load_image_file("profesora2.jpg")
profesor_face_encoding = face_recognition.face_encodings(profesor_image)[0]

#Ancho 1280 , se agrega una propiedad en el videocapture
cap.set(4,720)
#Largo 720, se agrega una propiedad en el videocapture
cap.set(5,680)
# FPS, se agregan los frames per second
#cap.set(6,10)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
contador = 0
process_this_frame = True


#mientras el video este abierto
while (cap.isOpened()):
    tiempo_actual = time.time()
    #diferencia_tiempo = tiempo_actual-tiempo_inicial
    testing += 1
    # Grab a single frame of video
    ret, frame = cap.read()
    #small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if process_this_frame:
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        #face_names = []
        #for face_encoding in face_encodings:
            #Search known face
            #match = face_recognition.compare_faces([profesor_face_encoding], face_encoding)
            #name = "KID"
            #if match[0]:
            #   name = "Profesor" 
            #face_names.append(name)
    process_this_frame = not process_this_frame
    
    # Loop through each face in this frame of video
    contador = 0
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        contador += 1
        for face_encoding in face_encodings:
            #Search known face
            match = face_recognition.compare_faces([profesor_face_encoding], face_encoding)
            name = "KID"
            if match[0]:
                name = "Profesor" 
        top += 20
        right += 20
        bottom += 20
        left += 20
        #Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        #name = "Face "+str(contador)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    if testing%200 == 0:
        process_this_frame = not process_this_frame

    #Guardamos contador para analizar despues
    datos_informe.append(contador)
    #Agregamos numero de ninios
    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = 2
    texto_caras = "Caras: " + str(contador)
    posicion = (20,40)
    color_texto = 255
    cv2.putText(frame,texto_caras, posicion, font,thickness, color_texto)
    if testing%5 == 0:    
        print("Processing frame",testing)
        tiempo_usado = time.time()-tiempo_inicial
        #Process kid looking the profesor
        excel_data.faces_to_excel(move_row=1, tiempo=int(tiempo_usado), caras=contador, carasMirando=contador-1)
    # Display the resulting image
    cv2.imshow('Video', frame)
    

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q') or testing > TEST_FLAG:
        break
cap.release()
cv2.destroyAllWindows()
