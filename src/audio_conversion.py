import ffmpeg
from pathlib import Path
def wav_to_ogg(input_file, filepath):
    input_file = Path.joinpath(filepath.parent, input_file)
    output_file = Path.joinpath(input_file.parent, "converted", input_file.name).with_suffix('.ogg')
    print(f"input = {input_file}\noutput = {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg.input(str(input_file)).output(str(output_file), aq=5).run()

def mass_conversion(input_dict, filepath):
    filepath = Path(filepath)
    for filename in input_dict.values():
        wav_to_ogg(filename, filepath)

if __name__ == "__main__":
    wav_to_ogg(r"C:\Users\Kondou\Documents\bms-compressor\test\[syatten] aliceblue (Radio Edit) (SP ANOTHER).wav")