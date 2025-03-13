import os
import ffmpeg
from pathlib import Path

ffmpeg_bin = 'ffmpeg.exe'  # Replace with the actual path

def check_video_length(input_file: Path):
    try:
        probe = ffmpeg.probe(input_file, ffmpeg_bin)
        duration = probe['streams'][0]['duration']
        if float(duration) < 1:
            return True
        else:
            return False
    except ffmpeg.Error as e:
        print(f"Error: {e}")
        return None

input_file = Path(r"C:\samplevid\video.mp4")
if check_video_length(input_file):
    print("The video is longer than 1 minute.")
else:
    print("The video is not longer than 1 minute.")