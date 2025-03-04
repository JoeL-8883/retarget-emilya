# Import libraries
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

'''
Converts the CSV data to numpy arrays that HumanML3D can convert to motion features.
This step takes a considerable amount of time.
'''

parser = argparse.ArgumentParser(
        description="Enter file/directory of CSV files.")
parser.add_argument("-d", "--dirname", type=str, help='Folder of .csv files for conversion.')
args = parser.parse_args()

dir_in = args.dirname # Path to directory

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

def process_arr(arr):
    to_delete = [0, 5, 10, 19, 24, 27]
    # Scale and normalise
    #arr = scale_distances(arr, 6.5)
    #arr = normalise(arr)

    # Delete joints
    arr = np.delete(arr, to_delete, axis=1)

    # Remap joints
    arr = remap(arr)

    return arr

def save_file(arr, dir):
    save_dir = os.path.join('./Convert-EMILYA/output', '3DPos')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filename = os.path.splitext(os.path.basename(dir))[0]
    output_path = os.path.join(save_dir, f'{filename}.npy')
    np.save(output_path, arr)

if not os.path.exists(dir_in):
    print("Error: folder {} not found.".format(dir_in))
    sys.exit(0)

# Convert csv files to numpy arrays
arr = csv_to_numpy(dir_in)

# Get the name of each file
filesnames = [f for f in os.listdir(dir_in) if f.endswith('.csv')]

for i, a in enumerate(arr):
    a = process_arr(a) # Remove and remap joints, scale and normalise
    a = a[::3] # Skip every other frame to make motion fater
    save_file(a, filesnames[i])
print("CSVs successfully converted.")




