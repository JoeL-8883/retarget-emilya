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

def csv_to_numpy(dir, single_file=False):
    if not single_file:
        csv_files = os.listdir(dir)
        csv_files = [f for f in csv_files if f.endswith('.csv')]
    else:
        csv_files = [dir]
    
    arrays = []

    for csv in csv_files:
        # Store csv as npy array
        arr = np.genfromtxt(os.path.join(dir, csv), delimiter=',', skip_header=1)

        # Remove time column
        arr = arr[:,1:]

        # Reshape array to frames, joints, 3D positions
        arr = arr.reshape(-1, 28, 3)
        arrays.append(arr)
    
    return arrays

def scale_distances(data, scale_factor=0.8):
    scaled_data = np.copy(data)
    for frame in range(data.shape[0]):
        for i in range(1, data.shape[1]):
            # Calculate the distance between the current joint and the previous joint
            distance = np.linalg.norm(data[frame, i] - data[frame, i-1])
            
            # Scale the distance
            scaled_distance = distance * scale_factor
            
            # Adjust the joint position based on the scaled distance
            direction = (data[frame, i] - data[frame, i-1]) / distance # Get the direction from the previous joint to the current joint
            scaled_data[frame, i] = scaled_data[frame, i-1] + direction * scaled_distance # Update position
    return scaled_data

def normalise(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalised = (data - min_val) / (max_val - min_val)
    normalised = normalised * 2 - 1

    return normalised

def remap(data):
    remap = {
            8: 0, 0: 1, 4: 2, 9: 3, 1: 4, 5: 5, 10: 6, 2: 7,
            6: 8, 11: 9, 3: 10, 7: 11, 20: 12, 12: 13, 16: 14,
            21: 15, 13: 16, 17: 17, 14: 18, 18: 19, 15: 20, 19: 21
        }

    remapped = np.zeros_like(data)

    for old, new in remap.items():
        remapped[:, new] = data[:, old]

    return remapped

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
    