import shutil
import os
import stat
from audio_conversion import to_ogg
# make sure subdir is absolute path
def process_files_subdirectory(subdir, output_path, base_path, in_place=False):
    if (subdir/ "processed_w") in subdir.iterdir():
        print("Already processed, skipping...")
    for file in subdir.iterdir():
        if file.is_file():
            if in_place:
                if file.suffix.lower() == '.wav':
                    to_ogg(file, base_path, base_path)
                    try:
                        os.remove(file)
                    except PermissionError:
                        os.chmod(file, stat.S_IWRITE)
                        os.remove(file)
            else:
                full_output_path = output_path / file.relative_to(base_path)
                if not full_output_path.exists():
                    full_output_path.mkdir(parents=True)
                if file.suffix.lower() == '.wav':
                    to_ogg(file, output_path, base_path)
                else:
                    #print(f"{file} -> {full_output_path}")
                    shutil.copy(file, full_output_path)
    open(subdir / "processed_w", 'a').close()
    print(f"finished processing {subdir}")
if __name__ == "__main__":
    raise Exception("This should not be ran independently.")
                
    