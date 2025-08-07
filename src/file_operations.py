import shutil
import os
import stat
import logging
from tqdm import tqdm
from audio_conversion import to_ogg
from video_conversion import to_mp4
from image_conversion import to_jpg

logger = logging.getLogger(__name__)
logging.basicConfig(filename='latest.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

# make sure subdir is absolute path
def process_files_subdirectory(subdir, output_path, base_path, in_place=False):
    if (subdir/ "processed_w") in subdir.iterdir():
        logger.info(f"processed_w found at {subdir}, skipping")
        return
    video_converted = False
    for file in tqdm(subdir.iterdir(), total=len(list(subdir.iterdir())), desc=f"{subdir.name}", unit="files", position=1, leave=False):
        if file.is_file():
            if in_place:
                if file.suffix.lower() == '.wav':
                    to_ogg(file, base_path, base_path)
                    try:
                        os.remove(file)
                    except PermissionError:
                        os.chmod(file, stat.S_IWRITE)
                        os.remove(file)
                if file.suffix.lower() in ['.mpg', '.avi', '.mp4', '.wmv', '.m1v', '.mpeg', '.m2v']:
                    # since the name might be changed, the file deletion will be handled in function
                    if video_converted:
                        logger.info("multiple videos detected, deleting the extra file...")
                        try:
                            os.remove(file)
                        except PermissionError:
                            os.chmod(file, stat.S_IWRITE)
                            os.remove(file)                        
                    else:
                        to_mp4(file, base_path, base_path) 
                        video_converted = True
                if file.suffix.lower() in ['.png', '.bmp', 'jpeg', 'jpg']:
                    # since the name might be changed, the file deletion will be handled in function
                    to_jpg(file, base_path, base_path) 
            else:
                full_output_path = output_path / file.relative_to(base_path)
                if not full_output_path.exists():
                    full_output_path.mkdir(parents=True)
                if file.suffix.lower() == '.wav':
                    to_ogg(file, output_path, base_path)
                if file.suffix.lower() in ['.mpg', '.avi', '.mp4', '.wmv', '.m1v', '.mpeg', '.m2v']:
                    # since the name might be changed, the file deletion will be handled in function
                    if video_converted:
                        logger.info("multiple videos detected, deleting the extra file...")
                        try:
                            os.remove(file)
                        except PermissionError:
                            os.chmod(file, stat.S_IWRITE)
                            os.remove(file)                        
                    else:
                        to_mp4(file, output_path, base_path) 
                        video_converted = True
                if file.suffix.lower() in ['.png', '.bmp', 'jpeg', 'jpg']:
                    # since the name might be changed, the file deletion will be handled in function
                    to_jpg(file, output_path, base_path) 
                else:
                    #print(f"{file} -> {full_output_path}")
                    shutil.copy(file, full_output_path)
    open(subdir / "processed_w", 'a').close()
    logger.info(f"finished processing {subdir}")
if __name__ == "__main__":
    raise Exception("This should not be ran independently.")
                
    