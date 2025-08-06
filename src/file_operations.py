import os
from audio_conversion import to_ogg
# make sure subdir is absolute path
def process_files_subdirectory(subdir, output_path, base_path):
    for file in subdir.iterdir():
        print(f"now on {file}")
        if file.is_file():
            if file.suffix.lower() in ['.ogg', '.wav']:
                to_ogg(file, output_path, base_path)
                
    