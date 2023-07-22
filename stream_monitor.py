# stream_monitor.py

import cv2
import time
from datetime import datetime

# Load the cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# To capture video from webcam
cap = cv2.VideoCapture(0)

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

while True:
    # Read the frame
    ret, img = cap.read()

    # If frame is read correctly
    if ret:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # If a face is detected, write the frame to file
        if len(faces) > 0:
            if out is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                out = cv2.VideoWriter(f'{timestamp}.avi', fourcc, 20.0, (640,480))

            out.write(img)

        # Else, if we have been writing a file, close it
        elif out is not None:
            out.release()
            out = None

    else:
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
if out is not None:
    out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
