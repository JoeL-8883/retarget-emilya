import argparse
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from util import check_file_shape, is_filetype

def create_animation(motion, filename, fps=60, frame_skip=2):
    # Create figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)

    # Set axis lables
    ax.set_xlabel('X')  
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Initialise scatter plot
    scatter = ax.scatter([], [], [], c='b', marker='o')

    # Used to track the coordinates of each joint in each frame
    def init():
        scatter._offsets3d = ([], [], [])
        return scatter,

    def update(frame):
        x = motion[frame, :, 0]
        y = motion[frame, :, 1]
        z = motion[frame, :, 2]
        scatter._offsets3d = (x, y, z) # The order of axes may need to be changed for better results
        return scatter,

    # Create animation
    ani = FuncAnimation(fig, update, frames=range(0, motion.shape[0], frame_skip), init_func=init, blit=True)

    # Save animation
    if not os.path.exists("output/animations"):
        os.makedirs("output/animations")
        
    output_path = os.path.join('output', 'animations', f'{filename}.gif')
    ani.save(output_path, fps=fps)

def check_file_shape(file):
    if file.shape[1] != 22 and file.shape[2] != 3:
        print("Error: file {} has incorrect shape.".format(file))
        sys.exit(0)

def is_npy(file, filename):
    if not file.endswith(".npy"):
        print(f"Warning, {filename} is not a npy file and will not be converted")
        return False
    return True

parser = argparse.ArgumentParser(
        description="Enter file/folder directory for conversion.")
parser.add_argument("-f", "--filename", type=str, help='.npy file for animation.')
parser.add_argument("-d", "--dirname", type=str, help='Folder of .npy files for animation.')
args = parser.parse_args()

file_in = args.filename
folder_in = args.dirname

if file_in:
    filename = file_in.split("/")[-1][:-4]
    if not os.path.exists(file_in):
        print("Error: file {} not found.".format(file_in))
        sys.exit(0)

    if is_filetype(file_in, filename, 'npy'):
        # Get the numpy array of the directory
        file_in = np.load(file_in)
        check_file_shape(file_in)
        create_animation(file_in, filename, fps=60, frame_skip=2)
        print("Animation created.")

elif folder_in:
    if not os.path.exists(folder_in):
        print("Error: folder {} not found.".format(folder_in))
        sys.exit(0)
    
    # For each file in the folder create an animation
    for file in os.listdir(folder_in):
        filename = file.split("/")[-1][:-4]
        file_dir = os.path.join(folder_in, file)

        if is_filetype(file_dir, filename, 'npy'):
            file_in = np.load(file_dir)
            check_file_shape(file_in)
            create_animation(file_in, filename, fps=60, frame_skip=1)
    print("Animations created.")
else:
    print("Error: no file or folder provided. To enter a file use -f {directory}, to enter a folder use -d {directory}.")
    sys.exit(0)

    