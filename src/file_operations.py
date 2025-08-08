import shutil
import os
import stat
import logging  
from audio_conversion import to_ogg
from video_conversion import to_mp4
from image_conversion import to_jpg
from pathlib import Path
logger = logging.getLogger(__name__)
logging.basicConfig(filename='latest.log' ,level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
# make sure subdir is absolute path
def list_files(subdir, files = []):
    for x in subdir.iterdir():
        if x.is_file():
            files.append(x)
        elif x.is_dir():
            list_files(x, files)
    return files
def process_files_subdirectory(subdir, output_path, base_path, in_place=False, ignore_processed=False):
    video_list = ['.mpg', '.avi', '.mp4', '.wmv', '.m1v', '.mpeg', '.m2v']
    image_list = ['.png', '.bmp', '.jpeg', '.jpg']
    if (subdir/ "processed_w") in subdir.iterdir() and not ignore_processed:
        logger.info(f"processed_w found at {subdir}, skipping")
        return
    video_converted = False
    if ignore_processed:
        video_list.remove('.mp4')
        image_list.remove('.jpg')
    for file in list_files(subdir):
        if file.is_file():
            if file.stem.endswith("_old"):
                try:
                    os.rename(file, file.with_stem(file.stem.replace("_old", "")))
                except FileExistsError:
                    pass
            if in_place:
                if file.suffix.lower() == '.wav':
                    to_ogg(file, base_path, base_path)
                    try:
                        os.remove(file)
                    except PermissionError:
                        os.chmod(file, stat.S_IWRITE)
                        os.remove(file)
                if file.suffix.lower() in video_list:
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
                if file.suffix.lower() in image_list:
                    # since the name might be changed, the file deletion will be handled in function
                    to_jpg(file, base_path, base_path) 
            else:
                full_output_path = output_path / file.relative_to(base_path)
                if not full_output_path.exists():
                    full_output_path.mkdir(parents=True)
                if file.suffix.lower() == '.wav':
                    to_ogg(file, output_path, base_path)
                if file.suffix.lower() in video_list:
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
                if file.suffix.lower() in image_list:
                    # since the name might be changed, the file deletion will be handled in function
                    to_jpg(file, output_path, base_path) 
                else:
                    #print(f"{file} -> {full_output_path}")
                    shutil.copy(file, full_output_path)
    open(subdir / "processed_w", 'a').close()
    logger.info(f"finished processing {subdir}")
if __name__ == "__main__":
    print(list_files(Path(r"G:\nythil bms pack\jp\hiragana_katakana_misc\りりくろ！")))
    #raise Exception("This should not be ran independently.")
                
    