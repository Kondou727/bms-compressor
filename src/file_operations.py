import shutil
from audio_conversion import to_ogg
from bms_file_reading import replace_file_extension
# make sure subdir is absolute path
def process_files_subdirectory(subdir, output_path, base_path):
    for file in subdir.iterdir():
        print(f"now on {file}")
        if file.is_file():
            full_output_path = output_path / file.relative_to(base_path)
            if file.suffix.lower() in ['.ogg', '.wav']:
                to_ogg(file, output_path, base_path)
            elif file.suffix.lower() in ['.bme', '.bms']:
                print(".bms/.bme file found, processing...")
                replace_file_extension(file, full_output_path, '.wav', '.ogg')
            else:
                print(f"{file} -> {full_output_path}")
                shutil.copy(file, full_output_path)


                
    