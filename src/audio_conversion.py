import ffmpeg
import logging
from constants import AQ
logger = logging.getLogger(__name__)
logging.basicConfig(filename='latest.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
# input file should be a Path object containing the absolute path of the input file
def to_ogg(input_file, output_path, base_path):
    relative_path = input_file.relative_to(base_path)
    output_file = output_path / relative_path.with_suffix('.ogg')
    logging.info(f"{input_file} -> {output_file}")
    if output_file.exists():
        logging.info("File already exists. Skipping...")
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        ffmpeg.input(str(input_file)).output(str(output_file), aq=AQ).global_args('-loglevel', 'quiet').run()
    except ffmpeg._run.Error as e:
        logging.warning(e)
    

if __name__ == "__main__":
    raise Exception("This should not be ran independently.")