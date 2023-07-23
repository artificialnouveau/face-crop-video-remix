import cv2
import dlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# Load the detector and the predictor
detector = dlib.get_frontal_face_detector()

# Video source
cap = cv2.VideoCapture('BlackOrWhite.mp4')

# Create a figure for plotting
fig = plt.figure()

# Lists to store individual trackers, axes and images for each face detected
trackers = []
axes = []
images = []

# Function to apply a simple "glitch" effect to an image
def glitch(img):
    # Copy the image
    img_glitched = img.copy()

    # Shift rows of pixels randomly to the right
    for i in range(img.shape[0]):
        img_glitched[i] = np.roll(img_glitched[i], shift=random.randint(-5, 5), axis=0)

    return img_glitched

# Function to update each frame
def update(i):
    # Read the next frame
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return

    # Convert frame to grayscale for detection (not needed for dlib but common for other detectors)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # If no faces are currently being tracked, detect faces
    if not trackers:
        faces = detector(gray)

        # For each face detected
        for rect in faces:
            # Initialize a new tracker for this face and start tracking
            tracker = dlib.correlation_tracker()
            tracker.start_track(frame, rect)
            trackers.append(tracker)

            # Random position for the new axis
            random_x = random.uniform(0, 1)
            random_y = random.uniform(0, 1)

            # Add a new axis for this face
            ax = fig.add_axes([random_x, random_y, 0.1, 0.1])
            ax.axis('off')  # Turn off axis lines and labels
            axes.append(ax)

            # Display the face in this axis
            img = ax.imshow(np.zeros((1, 1, 3)))
            images.append(img)

    # If faces are currently being tracked, update the trackers and display the faces
    else:
        for tracker, ax, img in zip(trackers, axes, images):
            # Update the tracker
            tracker.update(frame)

            # Get the position of the face
            pos = tracker.get_position()

            # Convert position to integers
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())

            # Crop the face
            crop = frame[startY:endY, startX:endX]

            # Enlarge the cropped face by a random factor to simulate zooming
            zoom_factor = random.uniform(1, 1.5)
            crop = cv2.resize(crop, None, fx=zoom_factor, fy=zoom_factor)

            # Apply the glitch effect
            crop = glitch(crop)

            # Update the image data
            img.set_data(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))

    # Draw the figure on the screen
    plt.draw()

# Animation object
ani = animation.FuncAnimation(fig, update, frames=range(100), repeat=False)

# Show the plot
plt.show()

# Release the video capture when everything is done
cap.release()
cv2.destroyAllWindows()
