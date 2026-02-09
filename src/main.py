from pathlib import Path
from capture import capture_frame

video = Path("sample/sample.mov")
output = Path("frames/frame_5s.png")

capture_frame(video, output, 5)
print("Done")
