import bms_file_reading
from pathlib import Path
from file_operations import process_files_subdirectory
from tqdm import tqdm
import os
import shutil
import logging
import time
from concurrent.futures import ProcessPoolExecutor
logger = logging.getLogger(__name__)
logging.basicConfig(filename='latest.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

def get_output_path(path):
    path = Path(path)
    # Go up one directory (.parent) then add "Converted" then add the last part
    converted_path = path.parent / "Converted" / path.name
    return converted_path
def main():
    base_path = Path(input("Enter bms folder path: ").strip())
    if not base_path.exists() or base_path == "":
        raise Exception("Path not found!")
    in_place = input("Should files be modified in-place (y) or outputted to a different folder (n): ").lower().strip()
    while (in_place not in ['y', 'n']):
        in_place = input("Input should only be y or n. Try again: ").lower().strip()
    if in_place == 'y':
        in_place = True
    else:
        in_place = False
    if in_place:
        output_path = base_path
    else:
        output_path = input("Enter output folder path (by default this will go into a converted folder): ").strip()
        if not output_path:
            print("No given output path, will be using default...")
            output_path = get_output_path(base_path)
            if not output_path.exists():
                output_path.mkdir(parents=True)
        else:
            output_path = Path(output_path)
        if not output_path.exists():
            raise Exception("Path not found!")
    ignore_processed = input("Reprocess all files? (this disables multithreading.) (y/n): ")
    while (ignore_processed not in ['y', 'n']):
        ignore_processed = input("Input should only be y or n. Try again: ").lower().strip()
    if ignore_processed == 'y':
        ignore_processed = True
    else:
        ignore_processed = False
    all_bms_path = bms_file_reading.list_all_files_with_extension(base_path, "bms") + bms_file_reading.list_all_files_with_extension(base_path, "bme")
    all_folder_path = bms_file_reading.get_all_relative_paths(all_bms_path)
    logger.info(f"base_path = {base_path}, output_path = {output_path} (should be same as base_path if in_place is true), in_place = {in_place}")

    # Use a ThreadPoolExecutor
    # max_workers can be adjusted based on your CPU cores and I/O speed
    # A common starting point is os.cpu_count() or higher for I/O-bound tasks
    if not ignore_processed:
        with ProcessPoolExecutor(max_workers=int(os.cpu_count()/2)) as executor:
            # Submit tasks to the executor
            # We use a list comprehension to create a list of futures
            futures = [executor.submit(process_files_subdirectory, bms_folder, output_path, base_path, in_place=in_place)
                       for bms_folder in sorted(all_folder_path)]

            # Use tqdm to show progress as futures complete
            for future in tqdm(futures, desc="Progress", unit="folders", position=0):
                # Calling .result() will re-raise any exceptions that occurred in the thread
                # and effectively waits for the future to complete.
                # You might want to add error handling here if process_files_subdirectory can fail.
                try:
                    future.result()
                except Exception as exc:
                    logger.error(f'Processing generated an exception: {exc}')

    for bms_folder in tqdm(sorted(all_folder_path), desc="Rechecking all folders...", unit="folders", position=0): # failsafe because multithread is buggy (IDK WHAT IM DOING)
        logger.info(f"Processing {bms_folder}...")
        process_files_subdirectory(bms_folder, output_path, base_path, in_place=in_place, ignore_processed=ignore_processed)


if __name__ == "__main__":
    if os.path.exists('latest.log'):
        shutil.copy('latest.log', f"{time.strftime("%Y%m%d-%H%M%S")}.log")
        open('latest.log', 'w').close()
    main()