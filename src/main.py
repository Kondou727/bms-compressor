import bms_file_reading
from pathlib import Path
from file_operations import process_files_subdirectory
def get_output_path(path):
    path = Path(path)
    # Go up one directory (.parent) then add "Converted" then add the last part
    converted_path = path.parent / "Converted" / path.name
    return converted_path
def main():
    base_path = Path(input("Enter bms folder path: ").strip())
    if not base_path.exists():
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
    all_bms_path = bms_file_reading.list_all_files_with_extension(base_path, "bms") + bms_file_reading.list_all_files_with_extension(base_path, "bme")
    all_folder_path = bms_file_reading.get_all_relative_paths(all_bms_path)
    for bms_folder in all_folder_path:
        print(f"Processing {bms_folder}...")
        process_files_subdirectory(bms_folder, output_path, base_path, in_place=in_place)


if __name__ == "__main__":
    main()