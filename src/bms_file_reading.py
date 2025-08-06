from pathlib import Path
import os
# filepath is absolute path to a specific file
'''def get_audio_files(filepath):
    filepath = Path(filepath)
    audio_files = set()
    with open(filepath, "r", encoding="latin-1") as file: # WTF?
        for line in file:
            if "MAIN DATA FIELD" in line:
                break
            if line.startswith("#WAV"):
                left, right = line.strip().split(maxsplit=1)
                audio_files.add(Path.joinpath(filepath.parent, right))
    return audio_files
'''
# subdir should be a path object, return list of absolute paths of audio files in the subdir
def get_audio_files(subdir):
    audio_files = []
    
    for file in Path.iterdir(subdir):
        if file.is_file() and file.suffix.lower() in ['.ogg', '.wav']:
            audio_files.append(file)
    
    return audio_files        
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

def replace_file_extension(filepath, input_extension, output_extension):
    with open(filepath, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(input_extension, output_extension)
    filepath = Path(filepath)
    with open(Path.joinpath(filepath.parent, "converted", filepath.name), 'w') as file:
        file.write(filedata)

if __name__ == "__main__":
    all_bms = list_all_files_with_extension(r"G:\nythil bms pack\eng\A", "bms")
    all_bms += list_all_files_with_extension(r"G:\nythil bms pack\eng\A", "bme")
    all_path = get_all_relative_paths(all_bms)
    for path in all_path:
        print(get_audio_files(path))