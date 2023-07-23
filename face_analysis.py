import os
import cv2
import dlib
import numpy as np
import subprocess
import sys

# Initialize dlib's face detector and the facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load video
input_video = sys.argv[1]
cap = cv2.VideoCapture(input_video)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Create output file names
filename = os.path.splitext(input_video)[0]
output_faces = filename + '_faces.avi'
output_leyes = filename + '_leyes.avi'
output_reyes = filename + '_reyes.avi'
output_mouths = filename + '_mouth.avi'

out_faces = cv2.VideoWriter(output_faces, fourcc, 20.0, (640,480))
out_leyes = cv2.VideoWriter(output_leyes, fourcc, 20.0, (640,480))
out_reyes = cv2.VideoWriter(output_reyes, fourcc, 20.0, (640,480))
out_mouths = cv2.VideoWriter(output_mouths, fourcc, 20.0, (640,480))

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

            # Check if regions have non-zero size before writing them to video
            if y2 - y1 > 0 and x2 - x1 > 0:
                # Face
                face_frame = frame[y1:y2, x1:x2]
                out_faces.write(face_frame)

            if landmarks.part(66).y - landmarks.part(48).y > 0 and landmarks.part(66).x - landmarks.part(48).x > 0:
                # Mouth
                mouth_frame = frame[landmarks.part(48).y:landmarks.part(66).y,
                                    landmarks.part(48).x:landmarks.part(66).x]
                out_mouths.write(mouth_frame)

            if landmarks.part(41).y - landmarks.part(36).y > 0 and landmarks.part(41).x - landmarks.part(36).x > 0:
                # Left Eye
                leye_frame = frame[landmarks.part(36).y:landmarks.part(41).y,
                                   landmarks.part(36).x:landmarks.part(41).x]
                out_leyes.write(leye_frame)

            if landmarks.part(47).y - landmarks.part(42).y > 0 and landmarks.part(47).x - landmarks.part(42).x > 0:
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
input = input_video
output = filename + '_output.mp4'

# Overlay faces
if os.path.getsize(output_faces) > 0:
    subprocess.run(['ffmpeg', '-i', input, '-i', output_faces, '-filter_complex', '[1:v]scale=iw/4:ih/4 [face]; [0:v][face]overlay=W-w:H:h', '-y', output])
    input = output

# Overlay left eye
if os.path.getsize(output_leyes) > 0:
    subprocess.run(['ffmpeg', '-i', input, '-i', output_leyes, '-filter_complex', '[1:v]scale=iw/4:ih/4 [leye]; [0:v][leye]overlay=0:H:h', '-y', output])
    input = output

# Overlay right eye
if os.path.getsize(output_reyes) > 0:
    subprocess.run(['ffmpeg', '-i', input, '-i', output_reyes, '-filter_complex', '[1:v]scale=iw/4:ih/4 [reye]; [0:v][reye]overlay=W-w:0', '-y', output])
    input = output

# Overlay mouth
if os.path.getsize(output_mouths) > 0:
    subprocess.run(['ffmpeg', '-i', input, '-i', output_mouths, '-filter_complex', '[1:v]scale=iw/4:ih/4 [mouth]; [0:v][mouth]overlay=0:0', '-y', output])

# Playback the output video
subprocess.run(['ffplay', output])
