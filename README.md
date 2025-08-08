
# bms-compressor

## what does it do
compresses image video and audio files given a root bms folder  
folders are categorized as "bms folders" if they have a .bms/.bme inside it


## how to run
get [uv](https://github.com/astral-sh/uv) and run `uv run src/main.py` at root directory

## to-do (if I feel like so)
multithread the file search
store the filesearch into maybe a text file, keeping track of the changes
a checker to make sure all the files listed in the bms are found
a less shitty progress bar

### info
small personal project for learning, will not fix bugs  
compression quality can be changed in `src/constants.py`  
existing .oggs are not re-encoded because I don't feel like the time trade-off would be worth it


