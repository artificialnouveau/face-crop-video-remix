# face_analysis.py

import os
import cv2
import dlib
import numpy as np
import subprocess

# Initialize dlib's face detector and the facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

for file in os.listdir():
    if file.endswith(".avi"):
        timestamp = file.split(".")[0]

        # Load video
        cap = cv2.VideoCapture(file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        out_faces = cv2.VideoWriter(f'{timestamp}_faces.avi', fourcc, 20.0, (640,480))
        out_leyes = cv2.VideoWriter(f'{timestamp}_leyes.avi', fourcc, 20.0, (640,480))
        out_reyes = cv2.VideoWriter(f'{timestamp}_reyes.avi', fourcc, 20.0, (640,480))
        out_mouths = cv2.VideoWriter(f'{timestamp}_mouth.avi', fourcc, 20.0, (640,480))

        #... (rest of the face_analysis.py)

        # Overlay the videos
        input = file
        output = f'{timestamp}_output.mp4'

        #... (rest of the face_analysis.py)

        # Play back the video
        os.system(f'ffplay -autoexit {output}')

