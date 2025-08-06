def get_audio_files(filepath):
    audio_files = {}
    with open(filepath, "r") as file:
        for line in file:
            if "MAIN DATA FIELD" in line:
                break
            if line.startswith("#WAV"):
                left, right = line.strip().split(maxsplit=1)
                audio_files[left] = right
    return audio_files

if __name__ == "__main__":
    print(get_audio_files(r"G:\nythil bms pack\eng\A\Absurd Gaff\_abs07_00_bmssp7e.bme"))