# Import libraries
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from util import csv_to_numpy, scale_distances, normalise, remap

'''
Converts the CSV data to numpy arrays that HumanML3D can convert to motion features.
This step takes a considerable amount of time.
'''

parser = argparse.ArgumentParser(
        description="Enter file/directory of CSV files.")
parser.add_argument("-d", "--dirname", type=str, help='Folder of .csv files for conversion.')
args = parser.parse_args()

dir_in = args.dirname # Path to directory

def process_arr(arr):
    to_delete = [0, 5, 10, 19, 24, 27]
    # Scale and normalise
    arr = scale_distances(arr)
    arr = normalise(arr)

    # Delete joints
    arr = np.delete(arr, to_delete, axis=1)

    # Remap joints
    arr = remap(arr)

    return arr

def save_file(arr, dir):
    if not os.path.exists("output/3Dpos"):
        os.makedirs("output/3Dpos")
    
    filename = os.path.splitext(os.path.basename(dir))[0]
    output_path = os.path.join('output', '3Dpos', f'{filename}.npy')
    np.save(output_path, arr)

if not os.path.exists(dir_in):
    print("Error: folder {} not found.".format(dir_in))
    sys.exit(0)

arr = csv_to_numpy(dir_in)

# Get the filename somewhere here
filesnames = [f for f in os.listdir(dir_in) if f.endswith('.csv')]

for i, a in enumerate(arr):
    a = process_arr(a)
    save_file(a, filesnames[i])
print("CSVs successfully converted.")




