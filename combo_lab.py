import cv2
import sys
import numpy as np

from skimage import io, color

# Create a VideoCapture object and get video from webcam
# 0 for internal, 1 for external
cap = cv2.VideoCapture(0)


# Create the haar cascade - used for lighting and stuff
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
def run():
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            #print("Found {0} faces!".format(len(faces)))


            #forehead = None
            L = 0
            A = 0
            B = 0

            for (x, y, w, h) in faces:
                rows = 0
                cols = 0

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # gets forehead from image and turns into lab

                # MIDDLE FACE REGION
                forehead = frame[y:y+150, x:x+w]
                rgb_forehead = cv2.cvtColor(forehead, cv2.COLOR_BGR2RGB)
                lab_forehead = color.rgb2lab(rgb_forehead)
                #
                rows = len(lab_forehead)
                cols = len(lab_forehead[0])
                for i in range(rows):
                    for j in range(cols):
                        #for w in range(len(lab_forehead[0][0])):
                        #    print(lab_forehead[i][j][w])
                        L += lab_forehead[i][j][0]
                        A += lab_forehead[i][j][1]
                        B += lab_forehead[i][j][2]
                numpix = rows*cols
                L = L/(numpix)
                A = A/(numpix)
                B = B/(numpix)

                # print("Lightness: ", L)
                # print("green-red: ", A)
                # print("blue-yellow: ", B)
            print(L)
            print(A)
            print(B)
            print("\n")

                # do we want L ??
                # # gets left cheek from image and turns into lab
                # left_cheek = image[y+150:y+h, x:x+100]
                # rgb_left_cheek = cv2.cvtColor(left_cheek, cv2.COLOR_BGR2RGB)
                # lab_left_cheek = color.rgb2lab(rgb_left_cheek)
                # # gets right cheek from image and turns into lab
                # right_cheek = image[y+150:y+h, x+180:x+w]
                # rgb_right_cheek = cv2.cvtColor(right_cheek, cv2.COLOR_BGR2RGB)
                # lab_right_cheek = color.rgb2lab(rgb_right_cheek)

            cv2.imshow('Video', frame)

            #print(forehead)



            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
run()
# When everything done, release the video capture object
cap.release()
