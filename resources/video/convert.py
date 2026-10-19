import os
import subprocess
from pathlib import Path

def is_h265(file_path):
    """Check if the video file uses H.265 codec using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        codec = result.stdout.strip()
        return codec == 'hevc'
    except Exception as e:
        print(f"Error checking codec for {file_path}: {e}")
        return False

def convert_to_h264(input_path):
    """Convert the video to H.264 in place using a temporary file."""
    input_path = Path(input_path)
    temp_path = input_path.with_name(f"temp_{input_path.name}")

    cmd = [
        'ffmpeg', '-y', '-i', str(input_path),
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
        '-c:a', 'copy',
        str(temp_path)
    ]

    print(f"Converting: {input_path}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        os.replace(temp_path, input_path)
        print(f"✔ Converted and replaced: {input_path}")
    else:
        print(f"❌ Failed to convert: {input_path}")
        if temp_path.exists():
            temp_path.unlink()

def convert_all_videos_in_folder(folder_path):
    """Scan and convert all H.265 videos in the given folder."""
    folder = Path(folder_path)

    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in ['.mp4', '.mkv', '.mov']:
            if is_h265(file):
                convert_to_h264(file)
            else:
                print(f"Skipping (not H.265): {file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python convert_h265_to_h264.py /path/to/folder")
        sys.exit(1)

    folder = sys.argv[1]
    convert_all_videos_in_folder(folder)

