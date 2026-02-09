import cv2
from pathlib import Path

def capture_frame(video_path, output_path, second):
    video = cv2.VideoCapture(str(video_path))
    video.set(cv2.CAP_PROP_POS_MSEC, second * 1000)

    success, frame = video.read()
    if not success:
        raise RuntimeError("Gagal ambil frame")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), frame)

    video.release()
