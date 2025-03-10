import os
import shutil

# Create dataset directories
current_dir = os.getcwd()
new_joint_vecs_dir = os.path.join(current_dir, 'new_joint_vecs')
texts_dir = os.path.join(current_dir, 'texts')

if not os.path.exists(new_joint_vecs_dir):
    os.makedirs(new_joint_vecs_dir)
if not os.path.exists(texts_dir):
    os.makedirs(texts_dir)

# Directories of datasets
emilya_dir = '/home/joe/project/Dataset/Emilya'
et2m_dir = '/home/joe/project/Dataset/EmotionalT2M/HumanML3D'

'''Get paths'''
# new_joints_vecs paths
emilya_dir_new_joint_vecs = os.path.join(emilya_dir, 'new_joint_vecs')
if not os.path.exists(emilya_dir_new_joint_vecs):
    raise FileNotFoundError(f'{emilya_dir_new_joint_vecs} does not exist')

et2m_dir_new_joint_vecs = os.path.join(et2m_dir, 'new_joint_vecs')
if not os.path.exists(et2m_dir_new_joint_vecs):
    raise FileNotFoundError(f'{et2m_dir_new_joint_vecs} does not exist')


# Check if dataset is empty to avoid duplication
if len(os.listdir('new_joint_vecs')) > 0 or len(os.listdir('texts')) > 0:
    raise FileExistsError('Dataset is not empty. Please clear the dataset before merging.')

'''Rename every file in Emilya dataset'''
'''
for file in os.listdir(emilya_dir_new_joint_vecs):
    file_dir = os.path.join(emilya_dir_new_joint_vecs, file)
    new_name = os.path.join(emilya_dir_new_joint_vecs, f'E{file}')
    os.rename(file_dir, new_name)
'''

'''Merge data'''
print("Copying new_joint_vecs from Emilya")
for file in os.listdir(emilya_dir_new_joint_vecs):
    file_dir = os.path.join(emilya_dir_new_joint_vecs, file)
    destination = os.path.join('new_joint_vecs', file)
    shutil.copy(file_dir, destination)

print("Copying new_joint_vecs from ET2M")
for file in os.listdir(et2m_dir_new_joint_vecs):
    file_dir = os.path.join(et2m_dir_new_joint_vecs, file)
    destination = os.path.join('new_joint_vecs', file)
    shutil.copy(file_dir, destination)
    
# Merge texts
print("Merging texts")
emilya_dir_texts = os.path.join(emilya_dir, 'texts')
et2m_dir_texts = os.path.join(et2m_dir, 'texts')

for file in os.listdir(emilya_dir_texts):
    file_dir = os.path.join(emilya_dir_texts, file)
    destination = os.path.join('texts', file)
    shutil.copy(file_dir, destination)

for file in os.listdir(et2m_dir_texts):
    file_dir = os.path.join(et2m_dir_texts, file)
    destination = os.path.join('texts', file)
    shutil.copy(file_dir, destination)

'''Write new text files'''
for file in ['all.txt', 'train.txt', 'val.txt', 'train_val.txt', 'test.txt']:
    for dir in [emilya_dir, et2m_dir]:
        with open(os.path.join(dir, file), 'r') as f:
            lines = f.readlines()
        with open(file, 'a') as f:
            f.writelines(lines)
print("Done.")
print(f'Number of files in new_joint_vecs: {len(os.listdir(new_joint_vecs_dir))}')
print(f'Number of files in texts: {len(os.listdir(texts_dir))}')

if len(os.listdir(new_joint_vecs_dir)) != len(os.listdir(texts_dir)):
    raise ValueError('Number of files in new_joint_vecs and texts do not match.')