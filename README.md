# Realtime Video Analysis Scripts

## Author
Artificial Nouveau

## Objective

This repository includes two Python scripts for realtime video analysis:

1. `stream_monitor.py`: Monitors a video stream and saves 1-minute clips whenever a person's face is detected.
2. `face_analysis.py`: Analyzes the saved clips, applies overlays for face, eyes, and mouth, and then plays back the video.

## Prerequisites

You'll need to have the following tools installed:

- Python 3
- OpenCV-Python
- Dlib
- Ffmpeg

To install the Python libraries, you can use pip:

```bash
pip install opencv-python-headless dlib ffmpeg
```

Also, you need to download the trained model file for the dlib's face detector. The file is called `shape_predictor_68_face_landmarks.dat` and you can download it from [here](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2). After downloading, extract it to the same directory as your Python scripts.

## Usage

First, run `stream_monitor.py` to start monitoring the video stream. 

```bash
python stream_monitor.py
```

The script will save 1-minute video clips whenever it detects a face in the video stream. The clips are saved in the AVI format with the timestamp of their start time as their filenames.

After you have collected some video clips, you can analyze them with `face_analysis.py`:

```bash
python face_analysis.py
```

The script processes each of the saved clips, overlays cropped face, eyes, and mouth videos at different corners, and then saves the result. The output videos are saved in the MP4 format with the original timestamp plus `_output` added to their filenames. After the processing of each clip, the result is played back using the `ffplay` command.

Please note that the face, eyes, and mouth videos are also saved with their respective names for further analysis or usage. 

Remember to adjust the scripts or the parameters used for face detection according to your camera setup and lighting conditions to achieve the best performance.


## Optional: Automate the Analysis Process

If you want `face_crop_video_remix.py` to automatically process a video clip as soon as it is created, you can use a tool such as [Watchdog](https://pypi.org/project/watchdog/). This Python library allows you to monitor a directory for file changes and trigger actions when a change occurs.

First, install the library with pip:

```bash
pip install watchdog
```

To run the script, use:

```bash
python auto_process.py
```

Please be aware that this script might lead to synchronization issues if new video clips are created faster than `face_crop_video_remix.py` can process them. You might need to implement a queuing system or use locks to handle such situations.
