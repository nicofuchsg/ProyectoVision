import cv2

import glob
import os.path as path

PHOTOS_DIR = 'Original_photos'
CHECKED_PHOTOS_DIR = 'Checked_photos'

# Marcamos imagenes en imagen dada
def mark_face(cascade, filepath):
    image = cv2.imread(filepath, cv2.IMREAD_COLOR)
    faces = cascade.detectMultiScale(image, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return image

default_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

filepaths = glob.glob(path.join(PHOTOS_DIR, '*.jpg'))
for filepath in filepaths:
    marked_image = mark_face(default_cascade, filepath)
    cv2.imwrite(path.join(CHECKED_PHOTOS_DIR, path.basename(filepath)), marked_image)