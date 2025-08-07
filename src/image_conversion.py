from PIL import Image
import os
import stat
import logging
from constants import JPG_QUALITY
logger = logging.getLogger(__name__)
logging.basicConfig(filename='latest.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
def to_jpg(input_file, output_path, base_path):
    relative_path = input_file.relative_to(base_path)
    output_file = output_path / relative_path.with_suffix('.jpg')
    logging.info(f"{input_file} -> {output_file}")    # if reprocessing or file is already jpg
    if output_file.exists():
        new_path = input_file.with_stem(input_file.stem + "_old")
        os.rename(input_file, input_file.with_stem(input_file.stem + "_old"))
        input_file = new_path

    img = Image.open(input_file)
    if img.mode != "RGB":
        img = img.convert("RGB")

    img.save(output_file, quality=JPG_QUALITY)
    
    try:
        os.remove(input_file)
    except PermissionError:
        os.chmod(input_file, stat.S_IWRITE)
        os.remove(input_file)

if __name__ == "__main__":
    raise Exception("This should not be ran independently.")