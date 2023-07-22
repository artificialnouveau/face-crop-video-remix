# face-crop-video-remix
# Face Crop Video Remix README

This Python script analyzes a video to detect faces and then crops the faces, mouths, left eyes, and right eyes of each person in the video. It then overlays these cropped sections onto the original video in each corner.

## Requirements

This script requires the following Python libraries:

- cv2
- dlib
- numpy

It also requires the dlib shape predictor data file `shape_predictor_68_face_landmarks.dat` to be in the same directory as the script. You can download it from the dlib sourceforge repository: http://dlib.net/files/

In addition, it requires ffmpeg for overlaying the cropped videos onto the original video. Please ensure that ffmpeg is installed and added to your PATH.

## Usage

The input video should be named `input_video.mp4` and be in the same directory as the script. The script will produce the output video as `output.mp4` in the same directory.

The script works as follows:

1. The script reads the input video frame by frame. For each frame, it uses the dlib face detector to find faces in the frame.
2. For each detected face, it uses the dlib shape predictor to find facial landmarks.
3. It then crops the face, mouth, left eye, and right eye from the frame based on these landmarks.
4. These cropped sections are written to separate video files: `faces.avi`, `mouth.avi`, `leyes.avi`, and `reyes.avi`.
5. After processing the entire video, it overlays the cropped videos onto the original video. The faces video is overlayed in the top right corner, the left eyes video is overlayed in the bottom left corner, the right eyes video is overlayed in the top left corner, and the mouths video is overlayed in the bottom right corner. Each overlay is 1/4 the size of the original video.
6. The overlayed video is written to `output.mp4`.

To run the script, navigate to the directory containing the script and the input video, and then use the following command:

```bash
python face_analysis.py
```

Please replace `face_analysis.py` with the actual filename of the script.

## Limitations

This script assumes that the video only contains one face. If the video contains more than one face, the script may produce unexpected results, as it doesn't handle multiple faces separately.

The script does not include any error checking or handling. If any issues occur during execution, such as the input video file not being found, or a face, mouth, or eye not being detected in a frame, the script may crash with an error. 

Finally, the size and position of the overlays are hardcoded in the script. If you want to use different sizes or positions, you will need to modify the script accordingly.
