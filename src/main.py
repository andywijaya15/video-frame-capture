import subprocess
from pathlib import Path

video = Path("video.mp4")
output_dir = Path("frames")
output_dir.mkdir(exist_ok=True)

interval = 5  # detik
duration_cmd = [
    "ffprobe", "-i", str(video),
    "-show_entries", "format=duration",
    "-v", "quiet", "-of", "csv=p=0"
]
duration = float(subprocess.check_output(duration_cmd).decode().strip())

t = 0
idx = 0
while t < duration:
    output_file = output_dir / f"frame_{idx:03d}.png"
    subprocess.run([
        "ffmpeg", "-ss", str(t), "-i", str(video),
        "-frames:v", "1", str(output_file),
        "-y", "-loglevel", "quiet"
    ])
    idx += 1
    t += interval

print(f"{idx} frames saved to {output_dir}")
