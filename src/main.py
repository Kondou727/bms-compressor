from audio_conversion import mass_conversion
from list_audio_files import get_audio_files

def main():
    path = r"c:\Users\Kondou\Documents\bms-compressor\test\Jack-the-Ripper◆\_jacktheripper_yume.bms"
    audio_files = get_audio_files(path)
    mass_conversion(audio_files, path)
    print("success!")

if __name__ == "__main__":
    main()