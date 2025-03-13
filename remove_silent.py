import subprocess
import re

def detect_silence(input_video, silence_log, silence_threshold=-50, min_silence_duration=0.5):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-af', f'silencedetect=n={silence_threshold}dB:d={min_silence_duration}',
        '-f', 'null', '-'
    ]
    with open(silence_log, 'w') as log_file:
        subprocess.run(command, stderr=log_file)

def parse_silence_log(silence_log):
    with open(silence_log, 'r') as log_file:
        lines = log_file.readlines()

    silence_starts = []
    silence_ends = []

    for line in lines:
        start_match = re.search(r'silence_start: (\d+\.\d+)', line)
        end_match = re.search(r'silence_end: (\d+\.\d+) \|', line)

        if start_match:
            silence_starts.append(float(start_match.group(1)))
        if end_match:
            silence_ends.append(float(end_match.group(1)))

    return silence_starts, silence_ends

def create_ffmpeg_concat_file(input_video, output_concat_file, silence_starts, silence_ends):
    with open(output_concat_file, 'w') as f:
        f.write("ffconcat version 1.0\n")
        current_position = 0.0
        for start, end in zip(silence_starts, silence_ends):
            if current_position < start:
                f.write(f"file '{input_video}'\n")
                f.write(f"inpoint {current_position}\n")
                f.write(f"outpoint {start}\n")
            current_position = end
        # Handle the last segment
        f.write(f"file '{input_video}'\n")
        f.write(f"inpoint {current_position}\n")
        f.write(f"outpoint {ffmpeg_get_duration(input_video)}\n")

def ffmpeg_get_duration(input_video):
    result = subprocess.run(
        ['ffmpeg', '-i', input_video, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout)

def concatenate_video(output_video, concat_file):
    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', concat_file, '-c', 'copy', output_video
    ]
    subprocess.run(command)

def remove_silent_parts(input_video, output_video, silence_threshold=-50, min_silence_duration=0.5):
    silence_log = 'silence_log.txt'
    output_concat_file = 'concat_file.txt'
    
    detect_silence(input_video, silence_log, silence_threshold, min_silence_duration)
    silence_starts, silence_ends = parse_silence_log(silence_log)
    create_ffmpeg_concat_file(input_video, output_concat_file, silence_starts, silence_ends)
    concatenate_video(output_video, output_concat_file)

# Example usage
remove_silent_parts("input_video.mp4", "output_video.mp4")
