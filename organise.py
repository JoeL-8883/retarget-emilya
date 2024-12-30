import os
import shutil
import argparse
import sys

'''
Organises the EMILYA dataset so it can be more easily converted then fitted to the 
HumanML3D data structure.
'''

parser = argparse.ArgumentParser(
    description="Enter directory of All_BvH_Files dataset")
parser.add_argument("-d", "--dirname", type=str, help='Directory of All_BvH_Files folder.')
args = parser.parse_args()
input_dir = args.dirname
outputdir = os.getcwd() 

if not os.path.isdir(input_dir):
    print("Error: folder {} not found.".format(input_dir))
    sys.exit(0)
elif not input_dir.endswith('All_BvH_Files'): 
    print("Warning: folder may not be correct. The folder name should be All_BvH_Files")

output_dir_raw = os.path.join(outputdir, 'output', 'BvH_files')
if not os.path.exists(output_dir_raw):
    os.makedirs(output_dir_raw)
counter = 1

# Get the motions in the input directory
emilya_motions = os.listdir(input_dir) # the different types of motions, i.e. SW

# Iterate through each of the motions, SW, BS, CS, etc.
for motion in emilya_motions:       
    if motion.endswith('.DS_Store'):
        continue
    else:
        motion_dir = os.path.join(input_dir, motion)
        emotions = os.listdir(motion_dir)

        # Iterate through each of the emotions, i.e. angry, happy, etc.
        for emotion in emotions[1:]:            
            # Get each of the actors mocap data for a motion and emotion
            actors_dir = os.path.join(input_dir, motion, emotion) # i.e. ../experiments/All_BvH_Files/SW/angry
            actors = os.listdir(actors_dir)

            # Get the directory of the actors mocap data containg BVH files
            for actor in actors:
                bvh_folder = os.path.join(actors_dir, actor)
                if bvh_folder.endswith('.DS_Store'): 
                    continue
                else:
                    bvh_files = os.listdir(bvh_folder)

                    # Copy the BVH files to the output directory
                    for bvh in bvh_files:
                        bvh_file = os.path.join(actors_dir, actor, bvh)
                        number = f"{counter:06d}"
                        final_destination_raw = os.path.join(output_dir_raw, number + '.bvh')
                        shutil.copy(bvh_file, final_destination_raw)
                        counter += 1
print(f"{counter} BvH files copied to {final_destination_raw[:-10]}")