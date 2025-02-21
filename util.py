import sys
import os
import numpy as np

def check_file_shape(file):
    if file.shape[1] != 22 and file.shape[2] != 3:
        print("Error: file {} has incorrect shape.".format(file))
        sys.exit(0)

def is_filetype(file, filename, filetype):
    if not file.endswith("." + filetype):
        print(f"Warning, {filename} is not a .{filetype} file and will not be converted")
        return False
    return True

def shorten_emotion(emotion):
    if emotion == 'Neutral':
        return 'Nt'
    elif emotion == 'Joy':
        return 'Jy'
    elif emotion == 'Anger':
        return 'Ag'
    elif emotion == 'Panic Fear':
        return 'PF'
    elif emotion == 'Anxiety':
        return 'Ax'
    elif emotion == 'Sadness':
        return 'Sd'
    elif emotion == 'Shame':
        return 'Sh'
    elif emotion == 'Pride':
        return 'Pr'
    else:
        print(f"Error: emotion {emotion} not recognised.")
    