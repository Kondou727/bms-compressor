from pathlib import Path
import os
# subdir should be a path object, return list of absolute paths of audio files in the subdir
def get_audio_files(subdir):
    audio_files = []
    
    for file in Path.iterdir(subdir):
        if file.is_file() and file.suffix.lower() in ['.ogg', '.wav']:
            audio_files.append(file)
    
    return audio_files

def get_necessary_files(bms):
    files = []
    with open(bms, "r") as file:
        for line in file:
            if "MAIN DATA FIELD" in line:
                break
            left, right = line.strip().split(maxsplit=1)
            if left in ["#BMP", "#WAV", "#OGG", "#BANNER", "#STAGEFILE"]:
                files.append(right)
    return files
# this returns the absolute path, like "G:\nythil bms pack\eng\A\Aztec Altar\436.bms"
def list_all_files_with_extension(path, extension): 
    output = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                output.append(os.path.join(root, file))
    return output

def get_all_relative_paths(paths):
    output = set()
    for path in paths:
        path = Path(path)
        output.add(path.parent)
    return output


if __name__ == "__main__":
    raise Exception("This should not be ran independently.")