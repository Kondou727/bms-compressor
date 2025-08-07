import ffmpeg
import subprocess
import os
import stat
from pathlib import Path
def to_mp4(input_file, output_path, base_path):
    relative_path = input_file.relative_to(base_path)
    output_file = output_path / relative_path.with_suffix('.mp4')
    print(f"{input_file} -> {output_file}")
    if output_file.exists():
        new_path = input_file.with_stem(input_file.stem + "_old")
        os.rename(input_file, input_file.with_stem(input_file.stem + "_old"))
        input_file = new_path
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg.input(str(input_file)).output(str(output_file), vcodec='libx264', preset="slow", crf=36, an=None).run()
    try:
        os.remove(input_file)
    except PermissionError:
        os.chmod(input_file, stat.S_IWRITE)
        os.remove(input_file)

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)




# 2 pass option for filesize
'''   bitrate = int(100000000 / get_length(input_file))
    ( # first pass
        ffmpeg
        .input(str(input_file))
        .output('NUL', vcodec='libx264', video_bitrate=bitrate, **{"pass" : 1}, an=None, f='null')
        .run(overwrite_output=True)

    )
    (   # second pass
        ffmpeg
        .input(str(input_file))
        .output(str(output_file), vcodec='libx264', video_bitrate=bitrate, **{"pass" : 2}, an=None)
        .run(overwrite_output=True)
    )'''


if __name__ == "__main__":
    to_mp4(Path(r"C:\Users\Kondou\Documents\bms-compressor\test\_bga.mp4"), Path(r"C:\Users\Kondou\Documents\bms-compressor\test\output"), Path(r"C:\Users\Kondou\Documents\bms-compressor\test"))