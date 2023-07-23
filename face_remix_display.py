import cv2
import dlib
import numpy as np
import random

# Function to apply a simple "glitch" effect to an image


def glitch(img, shift_range=5):
    img_glitched = img.copy()
    for i in range(img.shape[0]):
        img_glitched[i] = np.roll(
            img_glitched[i], shift=random.randint(-shift_range, shift_range), axis=0)
    return img_glitched


# Load the detector
detector = dlib.get_frontal_face_detector()

# Video source
cap = cv2.VideoCapture('./BlackOrWhite.mp4')

# Constants for defining cropped image size
IMG_SIZE = (100, 100)

# Constants for defining the display size
DISPLAY_SIZE = (300, 300)

# Video writer with reduced FPS for a slower video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
# Lower the FPS from 20.0 to 10.0 to slow down the video
out = cv2.VideoWriter('output.mp4', fourcc, 10.0, DISPLAY_SIZE)

# Variables to hold the last few processed frames
last_images = []
last_image_index = 0
num_last_images = 10  # The number of last images to keep track of

# Flag to ignore initial frames until the first face is detected
first_face_detected = False

while cap.isOpened():
    # Initialize current_frame as an empty image
    current_frame = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), dtype='uint8')

    # Read the next frame
    ret, frame = cap.read()

    if not ret:  # If we're out of frames, end the loop
        break

    # Convert frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    cropped_images = []  # List to store the cropped images

    if faces:  # If faces are detected
        first_face_detected = True  # Set the flag
        for rect in faces:
            startX = rect.left()
            startY = rect.top()
            endX = rect.right()
            endY = rect.bottom()

            # Crop the face
            crop = frame[startY:endY, startX:endX]

            # Check if the cropped image is not empty
            if crop.size == 0:
                continue

            # Resize the cropped face to a standard size
            crop = cv2.resize(crop, IMG_SIZE)

            # Apply the glitch effect
            crop = glitch(crop)

            # Apply a Gaussian blur for smoothing
            crop = cv2.GaussianBlur(crop, (5, 5), 0)

            # Append the cropped image to the list
            cropped_images.append(crop)

            # Update the list of last images
            if len(last_images) >= num_last_images:
                last_images.pop(0)  # Remove the oldest frame if we've reached the limit
            last_images.append(crop)  # Add the current image to the end
            last_image_index = len(last_images) - 1  # The last image is now the current one
    elif first_face_detected:  # If no faces are detected, but we've seen at least one face before
        last_image_index -= 1  # Go to the previous image
        if last_image_index < 0:
            # Loop back to the end if we've reached the start
            last_image_index = len(last_images) - 1
        if last_images:
            # Add the last image to the cropped_images
            cropped_images.append(last_images[last_image_index])

    # Process the images based on the number of detected or reused faces
    if len(cropped_images) == 1:
        current_frame = np.vstack([cropped_images[0]] * 3)
    elif len(cropped_images) == 2:
        current_frame = np.vstack((np.hstack((cropped_images[0], cropped_images[1])),
                                   np.hstack((cropped_images[0], cropped_images[1]))))
    elif len(cropped_images) >= 3:
        current_frame = np.vstack((np.hstack((cropped_images[0], cropped_images[1], cropped_images[2])),
                                   np.hstack(
                                       (cropped_images[0], cropped_images[1], cropped_images[2])),
                                   np.hstack((cropped_images[0], cropped_images[1], cropped_images[2]))))

    # Resize the image to the display size
    current_frame = cv2.resize(current_frame, DISPLAY_SIZE)

    # Write the frame to the output file before displaying
    out.write(current_frame)

    # Display the images
    cv2.imshow("Faces", current_frame)

    # Check if the user wants to quit
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the video capture and writer when everything is done
cap.release()
out.release()
cv2.destroyAllWindows()
