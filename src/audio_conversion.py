import ffmpeg
from pathlib import Path
# input file should be a Path object containing the absolute path of the input file
def to_ogg(input_file, output_path, base_path):
    relative_path = input_file.relative_to(base_path)
    output_file = output_path / relative_path.with_suffix('.ogg')
    print(f"{input_file} -> {output_file}")
    if output_file.exists():
        print("File already exists. Skipping...")
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        ffmpeg.input(str(input_file)).output(str(output_file), aq=5).global_args('-n').run(quiet=True)
    except ffmpeg._run.Error as e:
        print(e)
    

    

if __name__ == "__main__":
    pass