import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class NewClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f'New clip: {event.src_path}')  
        subprocess.run(['python', 'face_crop_video_remix.py', event.src_path])

if __name__ == "__main__":
    event_handler = NewClipHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
