# Contributors: Will Walbers, Kiril Kuzmanovski, Muhammed Imran Anthony Nepomuceno
# Publication Date: 2/28/2019
# Description: This program records video from webcam, converts it into LAB color space
# and outputs a video file.

import cv2
import sys
import numpy as np
import math
from skimage import io, color

# Create a VideoCapture object and get video from webcam
# 0 for HD(if connected, otherwise internal), 1 for internal (if HD connected)
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (640,480))

# Create the haar cascade - used for lighting and stuff
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            L = 0
            A = 0
            B = 0
            rows = 0
            cols = 0
            # Draws rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #forehead = frame[y:y+90, x:x+w]
            #cv2.rectangle(frame, (x, y), (x+w, y+80), (0,255,0),2)
            # gets forehead from image and turns into lab
            face_frame = frame[y:y+h, x:x+w]
            rgb_face = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
            lab_face = color.rgb2lab(rgb_face)

            # Gets dimension of face_frame
            rows = len(lab_face)
            cols = len(lab_face[0])

            # Thresholds: 6N lounge, test_vid1, 2, and 3 = 7
            threshold = 7
            gain = 0.8
            for i in range(rows):
                for j in range(cols):
                    if((lab_face[i][j][1] > threshold)):
                        # print(lab[i][j][1])
                        face_frame[i][j][0] = 0
                        face_frame[i][j][1] = 0
                        # Colors red channel where 255 is light and 0 is darker
                        face_frame[i][j][2] = 255 - (gain * lab_face[i][j][1]) * (255/25)


        # Saves frame to video output
        out.write(frame)
        # Displays frame
        cv2.imshow('Video', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # If receiving input from file, then processes until exit key or has read all frames
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break
    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()
out.release()
cv2.destroyAllWindows()
