import os
import cv2
import dlib
import numpy as np
import subprocess

# Initialize dlib's face detector and the facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load video
cap = cv2.VideoCapture('input_video.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out_faces = cv2.VideoWriter('faces.avi', fourcc, 20.0, (640,480))
out_leyes = cv2.VideoWriter('leyes.avi', fourcc, 20.0, (640,480))
out_reyes = cv2.VideoWriter('reyes.avi', fourcc, 20.0, (640,480))
out_mouths = cv2.VideoWriter('mouth.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

        # Use detector to find face landmarks
        faces = detector(gray)

        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            landmarks = predictor(image=gray, box=face)

            # Face
            face_frame = frame[y1:y2, x1:x2]
            out_faces.write(face_frame)

            # Mouth
            mouth_frame = frame[landmarks.part(48).y:landmarks.part(66).y,
                                landmarks.part(48).x:landmarks.part(66).x]
            out_mouths.write(mouth_frame)

            # Left Eye
            leye_frame = frame[landmarks.part(36).y:landmarks.part(41).y,
                               landmarks.part(36).x:landmarks.part(41).x]
            out_leyes.write(leye_frame)

            # Right Eye
            reye_frame = frame[landmarks.part(42).y:landmarks.part(47).y,
                               landmarks.part(42).x:landmarks.part(47).x]
            out_reyes.write(reye_frame)

    else:
        break

# Release everything when job is finished
cap.release()
out_faces.release()
out_leyes.release()
out_reyes.release()
out_mouths.release()

# Overlay the videos
input = "input_video.mp4"
output = "output.mp4"

# Overlay faces
if os.path.isfile('faces.avi'):
    subprocess.run(['ffmpeg', '-i', input, '-i', 'faces.avi', '-filter_complex', '[1:v]scale=iw/4:ih/4 [face]; [0:v][face]overlay=W-w:H:h', output])
    input = output

# Overlay left eye
if os.path.isfile('leyes.avi'):
    subprocess.run(['ffmpeg', '-i', input, '-i', 'leyes.avi', '-filter_complex', '[1:v]scale=iw/4:ih/4 [leye]; [0:v][leye]overlay=0:H:h', output])
    input = output

# Overlay right eye
if os.path.isfile('reyes.avi'):
    subprocess.run(['ffmpeg', '-i', input, '-i', 'reyes.avi', '-filter_complex', '[1:v]scale=iw/4:ih/4 [reye]; [0:v][reye]overlay=W-w:0', output])
    input = output

# Overlay mouth
if os.path.isfile('mouth.avi'):
    subprocess.run(['ffmpeg', '-i', input, '-i', 'mouth.avi', '-filter_complex', '[1:v]scale=iw/4:ih/4 [mouth]; [0:v][mouth]overlay=0:0', output])
