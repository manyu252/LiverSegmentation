########################################
#
# This script combines liver and hepatic vessel segmentations into a single NIfTI file for each case.
#
# author: Abhimanyu Anand (Abhi)
# email: manyu252@gmail.com
#
# Usage: python src/createCombinedSegmentation.py
#
# Note: Change the local paths of the datasets to be used to combine.
# Note: The filenames are the same in both the datasets for easier use. Change this part of the code if required in the future.
# Note: The classes of the segmetations to be combined are also hard coded. Change them if required.
#
# Read the README file for better understanding.
#
########################################

import os
import time

import nibabel as nib
import numpy as np

liver_seg_dir = '/workspace/Datasets/MSD/Task08_HepaticVessel_Liver_Contours'
vessel_seg_dir = '/workspace/Datasets/MSD/Task08_HepaticVessel/labelsTr'
combined_seg_dir = '/workspace/Datasets/MSD/Task08_HepaticVessel/combinedLabels'

for file in sorted(os.listdir(liver_seg_dir)):
    file_no = int(''.join(filter(str.isdigit, file)))
    liver_seg_file = os.path.join(liver_seg_dir, file)
    # print(f'liver seg file: {liver_seg_file}')

    # Load the liver segmentation NIfTI file
    liver_seg_img = nib.load(liver_seg_file)
    liver_seg_data = liver_seg_img.get_fdata()

    # Load the hepatic vessels segmentation NIfTI file
    vessel_seg_file = os.path.join(vessel_seg_dir, file)
    vessel_seg_img = nib.load(vessel_seg_file)
    vessel_seg_data = vessel_seg_img.get_fdata()
    # print(f'vessel seg file: {vessel_seg_file}')

    # liver_seg_data uses 5 for liver tissue, and similarly vessel_seg_data uses 2 for vessels

    # Initial label is 0 (background)
    combined_seg_data = np.zeros_like(liver_seg_data)
    combined_seg_data = combined_seg_data.astype(int)

    # Assign 1 to liver tissue areas, ensure you don't overwrite vessels
    combined_seg_data[np.where(liver_seg_data == 5)] = 1

    # Assign 2 to hepatic vessels, overwrite liver label if necessary
    combined_seg_data[np.where(vessel_seg_data == 1)] = 2

    # Save the new NIfTI combined image using the original liver segmentation file affine and header
    new_img = nib.Nifti1Image(combined_seg_data, liver_seg_img.affine, liver_seg_img.header)
    combined_seg_file_name = f'liver_hepatic_vessel_{file_no:03d}.nii.gz'
    combined_seg_save_path = os.path.join(combined_seg_dir, combined_seg_file_name)
    nib.save(new_img, combined_seg_save_path)

    print(f'Saved file {combined_seg_save_path}')