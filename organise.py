import os
import shutil
import argparse
import sys
import random
from util import shorten_emotion

'''
Copy all the BvH files into a single directory, and write captions for each motion.
'''

parser = argparse.ArgumentParser(
    description="Enter directory of All_BvH_Files dataset")
parser.add_argument("-d", "--dirname", type=str, help='Directory of All_BvH_Files folder.')
args = parser.parse_args()
input_dir = args.dirname # directory of the All_BvH_Files folder containing motions
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

# Create captions (descriptions for each motion) and texts (generic descriptions of each type of motion)
captions_dir = os.path.join(outputdir, 'captions')
if not os.path.exists(captions_dir):
    os.makedirs(captions_dir)

texts_dir = os.path.join(outputdir, 'texts') # this should already exist


# Get the motions in the input directory
emilya_motions = os.listdir(input_dir) # the different types of motions, i.e. SW

# Iterate through each of the motions, SW, BS, CS, etc.
for motion in emilya_motions:       
    if motion.endswith('.DS_Store') or motion == 'SDBS' or motion == 'CS':
        continue
    else:
        motion_dir = os.path.join(input_dir, motion)
        emotions = os.listdir(motion_dir)

        # Iterate through each of the emotions, i.e. angry, happy, etc.
        for emotion in emotions[1:]:
            emotion_dir = os.path.join(motion_dir, emotion)

            # Get each of the actors mocap data for a motion and emotion
            actors = os.listdir(emotion_dir)
            
            # Get the directory of the actors mocap data containg BVH files
            for actor in actors:
                bvh_dir = os.path.join(emotion_dir, actor)
                if bvh_dir.endswith('.DS_Store'): 
                    continue
                else:
                    bvh_files = os.listdir(bvh_dir)

                    # Copy the BVH files to the output directory
                    for bvh in bvh_files:
                        bvh_file = os.path.join(bvh_dir, bvh)

                        # Create file name
                        number = f"{counter:06d}"
                        final_destination_raw = os.path.join(output_dir_raw, number + '.bvh')
                        
                        # Copy file
                        shutil.copy(bvh_file, final_destination_raw)
                        
                        ''' Create captions each motion '''
                        # Get location of relevant descriptions
                        emotion_abbv = shorten_emotion(emotion)
                        emotion_caption = motion+emotion_abbv+'.txt' # i.e. SWangry.txt
                        text_dir = os.path.join(texts_dir, emotion_caption)
                            
                        with open(text_dir, 'r') as f:
                            lines = f.readlines()

                        captions = random.sample(lines, 3)
         
                        # Write captions to file
                        caption_filename = number + '.txt'
                        caption_file = os.path.join(captions_dir, caption_filename)

                        with open(caption_file, 'w') as f:
                            for c in captions:
                                f.write(c.strip() + '\n')

                        counter += 1

                    
print(f"{counter} BvH files copied to {final_destination_raw[:-10]}")