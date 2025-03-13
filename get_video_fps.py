import os
import ffmpeg
from pathlib import Path

def speed_up_video(input_file: Path, output_file: Path):
    """
    Speeds up the playback of the given video file to fit a maximum duration of 59 seconds.

    Args:
    input_file (Path): Path to the input video file.
    output_file (Path): Path to the output video file.
    """
    # Calculate the new duration in seconds
    duration = 59

    # Calculate the new speed factor
    speed = input_file.stat().st_size / (duration * 1000 * 1000)

    # Call ffmpeg to speed up the video
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
    os.environ['PATH'] = f'{os.path.dirname(ffmpeg_path)};{os.environ["PATH"]}'
    (
        ffmpeg
        .input(str(input_file))
        .filter("setpts", f"{1/speed}*PTS")
        .output(str(output_file), vcodec="libx264", crf=18, acodec="aac")
        .run(overwrite_output=True)
    )

input_file = Path(r"C:\samplevid\video.mp4")
output_file = Path(r"C:\samplevid\video_speedup.mp4")

if input_file.exists() and input_file.stat().st_size > 1e6:  # 1 MB
    speed_up_video(input_file, output_file)
    print(f"The video has been speeded up and saved to {output_file}")
else:
    print(f"The video is already shorter than 1 minute or does not exist: {input_file}")