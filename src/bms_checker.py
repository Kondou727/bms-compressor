from bms_file_reading import get_necessary_files
from pathlib import Path    
def integrity_check(bms): # bms is path object
    file_list = get_necessary_files(bms)
    for file in file_list:
        file_path = bms.parent / file
        if not file_path.exists():
            pass
        