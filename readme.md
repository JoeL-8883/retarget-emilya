# Retargeting Emilya for HumanML3D

Follow the steps below to integrate the Emilya dataset into HumanML3D:

1. **Obtain the Dataset**  
   Request the Emilya dataset from Catherine Pelachaud. catherine.pelachaud@sorbonne-universite.fr

2. **Extract Motion Data Hierarchy**  
    To extract the BVH motion data from the Emilya hierarchy, run 
```python
   python organise.py '[directory to BVH files]'
```
    This script also assigns captions and splits the data into training, validation, and testing sets.

3. **Convert BVH to CSV**  
   Use the conversion scripts by tekulvw to convert the BVH files to CSV format.
https://github.com/tekulvw/bvh-converter

4. **Convert CSV Files and Re-target Data**  
    Convert all CSV to NumPy arrays and retarget the data to SMPL
```python
    python retarget.py ['directory to all CSV files']
```

5. **Calculate Data Statistics and Motion Features**  
   In the HumanML3D repository:
   - Run `cal_mean_variance.ipynb` to calculate the mean and standard deviation of the Emilya dataset.
   - Run `motion_representation.ipynb` to convert sequential joint position data into motion features.

6. **Integrate into HumanML3D**  
   Replace the existing data in HumanML3D with the newly processed Emilya data.
