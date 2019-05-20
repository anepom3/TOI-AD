import cv2
import sys

# Get user supplied values
imagePath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
#    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    flags = cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #    forehead = image[y:((y+h)/4), (x+(x/5)):((x+w)-((x+w)/5))]
    forehead = image[y:y+90, x:x+w]
    left_cheek = image[y+150:y+h, x:x+100]
    right_cheek = image[y+150:y+h, x+180:x+w]

print(type(forehead))
#cv2.imshow("Faces found", image)
cv2.imwrite("square_face.png", image)
cv2.imwrite("forehead.png", forehead)
cv2.imwrite("left_cheek.png", left_cheek)
cv2.imwrite("right_cheek.png", right_cheek)
cv2.waitKey(0)
