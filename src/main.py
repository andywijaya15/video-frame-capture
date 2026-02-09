import cv2
import numpy as np
from pathlib import Path
from nudenet import NudeDetector

# paths
video_path = Path("sample/sample.mov")
output_dir = Path("best_frames_safe")
output_dir.mkdir(exist_ok=True)

# init nudity detector
detector = NudeDetector()

# OpenCV video
cap = cv2.VideoCapture(str(video_path))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

best_score = 0
best_frame = None
best_frame_idx = 0

for i in range(frame_count):
    ret, frame = cap.read()
    if not ret:
        break

    # cek nudity
    temp_file = output_dir / "temp_check.png"
    cv2.imwrite(str(temp_file), frame)
    detections = detector.detect(str(temp_file))
    temp_file.unlink()  # hapus sementara

    nudity = False
    for d in detections:
        if d["score"] >= 0.6:
            nudity = True
            break
    if nudity:
        continue  # skip frame NSFW

    # hitung score brightness + sharpness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    score = brightness*0.5 + sharpness*0.5

    if score > best_score:
        best_score = score
        best_frame = frame
        best_frame_idx = i

cap.release()

# simpan frame terbaik yang aman
if best_frame is not None:
    seconds = best_frame_idx / fps
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    timestamp_str = f"{hours:02d}-{minutes:02d}-{secs:02d}"

    output_file = output_dir / f"best_safe_frame_{timestamp_str}.png"
    cv2.imwrite(str(output_file), best_frame)
    print(f"Best safe frame saved: {output_file} (score: {best_score:.2f})")
else:
    print("No safe frame detected!")
