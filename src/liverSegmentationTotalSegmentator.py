##################################################################
#
# This script is used to run the TotalSegmentator on a nifti file
# and calculate the DICE score between the output of the TotalSegmentator
# and the ground truth segmentation file.
#
##################################################################


import sys
import os

import numpy as np
import nibabel as nib
from totalsegmentator.python_api import totalsegmentator

def runTotalSegmentator(input_file, output_path):
    totalsegmentator(input_file, output_path, fast=True, ml=True, roi_subset=['liver'])

def calculateDICEScore(input_file, output_file):
    nifti1_img = nib.load(input_file)
    nifti2_img = nib.load(output_file)

    # Extract the data from the NIfTI objects
    nifti1_data = nifti1_img.get_fdata()
    nifti2_data = nifti2_img.get_fdata()

    # Assuming you know the label values
    label_in_first_file = 5  # Example label value in your first NIfTI file
    label_in_second_file = 1  # Assuming the label in your second file is 1

    # Creating binary masks for the labels of interest
    mask1 = np.where(nifti1_data == label_in_first_file, 1, 0)
    mask2 = np.where(nifti2_data == label_in_second_file, 1, 0)

    intersection = np.sum(mask1 * mask2)
    size1 = np.sum(mask1)
    size2 = np.sum(mask2)

    dice_score = (2. * intersection) / (size1 + size2)

    print("Dice score:", dice_score)
    return dice_score

def main():
    input_file = sys.argv[1]
    seg_path = sys.argv[2]
    output_path = 'temp/'
    os.makedirs(output_path, exist_ok=True)

    # check if input is a file
    if os.path.isfile(input_file):
        filename = os.path.basename(input_file)

        # run the total segmentator on the file
        print(f'\nRunning TotalSegmentator on {filename}')
        runTotalSegmentator(input_file, os.path.join(output_path, filename))

        # calculate the dice score
        print(f'\nCalculating DICE score for {filename}')
        print(f'Using {seg_path}')
        dice = calculateDICEScore(os.path.join(output_path, filename), seg_path)

    # check if input is a directory
    elif os.path.isdir(input_file):
        # open a new csv file to save the input file, segmentation file and the dice score
        with open('temp/dice_scores.csv', 'w') as f:
            f.write('File-No, Input File, Segmentation File, Dice Score\n')

        # loop through all the files in the input directory
        for file in os.listdir(input_file):
            try:
                # check if the file is a nifti file
                if file.endswith('.nii') or file.endswith('.nii.gz'):
                    # run the total segmentator on the file
                    print(f'\nRunning TotalSegmentator on {file}')
                    runTotalSegmentator(os.path.join(input_file, file), os.path.join(output_path, file))

                    # get the file number from the file name
                    file_no = int(''.join(filter(str.isdigit, file)))
                    seg_file = f'segmentation-{file_no}.nii'    
                    print(f'\nCalculating DICE score for {file}')
                    print(f'Using {seg_file}')

                    # calculate the dice score
                    dice = calculateDICEScore(os.path.join(output_path, file), os.path.join(seg_path, f'segmentation-{file_no}.nii'))

                    # write the input file, segmentation file and the dice score to the csv file
                    with open('temp/dice_scores.csv', 'a') as f:
                        f.write(f'{file_no}, {file}, {seg_file}, {dice}\n')
            except Exception as e:
                print(f'Error processing {file}: {e}')

if __name__ == '__main__':
    main()