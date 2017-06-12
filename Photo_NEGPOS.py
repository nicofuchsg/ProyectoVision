import cv2

import glob
import os
import os.path as path

PHOTOS_DIR = 'Original_photos'
NEGATIVE_PHOTOS_DIR = 'negative_photos'

# list files for training
POSITIVE_LIST_FILENAME = 'positive.txt'
NEGATIVE_LIST_FILENAME = 'negative.txt'

# extract facial regions from given image,
# and return the largest
def detect_face(cascade, filepath):
    image = cv2.imread(filepath, 0)
    faces = cascade.detectMultiScale(image, 1.3, 5)

    face = None
    for (x, y, w, h) in faces:
        if face is None or w * h > face[2] * face[3]:
            face = (x, y, w, h)

    if face is None:
        return filepath, 0, None
    else:
        return filepath, 1, face

default_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# (positive) iterate all images
pfilepaths = glob.glob(path.join(PHOTOS_DIR, '*.jpg'))
print 'Iterating ' + str(len(pfilepaths)) + ' positive files...'
num_detected = 0
positive_file = open(POSITIVE_LIST_FILENAME, 'w')
for filepath in pfilepaths:
    fpath, count, region = detect_face(default_cascade, filepath)
    if region != None:
        num_detected += 1
        line = ' '.join((fpath, str(count), str(region[0]), str(region[1]), str(region[2]), str(region[3])))
        positive_file.write(line + '\n')
positive_file.close()

# (negative) iterate all images
nfilepaths = glob.glob(path.join(NEGATIVE_PHOTOS_DIR, '*.jpg'))
print 'Iterating ' + str(len(nfilepaths)) + ' negative files...'
negative_file = open(NEGATIVE_LIST_FILENAME, 'w')
for filepath in nfilepaths:
    negative_file.write(filepath + '\n')
negative_file.close()

# print result
print 'Total ' + str(num_detected) + '/' + str(len(pfilepaths)) + ' positive images, ' + str(len(nfilepaths)) + ' negative images'