##################################################################
#
# This script is used to run the TotalSegmentator on a nifti file
# and calculate the DICE score between the output of the TotalSegmentator
# and the ground truth segmentation file.
#
# author: Abhimanyu Anand (Abhi)
# email: manyu252@gmail.com
#
# Usage:
# # Single file mode: python3 src/liverSegmentationTotalSegmentator.py <input_file.nii> <ground_truth_segmentation.nii>[OPTIONAL]
# # Directory mode: python3 src/liverSegmentationTotalSegmentator.py <input_directory> <ground_truth_directory>[OPTIONAL]
#
##################################################################


import sys
import os
import time

import numpy as np
import nibabel as nib
from totalsegmentator.python_api import totalsegmentator

def runTotalSegmentator(input_file, output_path):
    # For CPU usage (local)
    # totalsegmentator(input_file, output_path, fast=True, ml=True, roi_subset=['liver'])

    # For GPU usage (in scalpel)
    totalsegmentator(input_file, output_path, ml=True)

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
    try:
        seg_path = sys.argv[2]
    except:
        seg_path = None
    output_path = 'temp/'
    os.makedirs(output_path, exist_ok=True)

    # check if input is a file
    if os.path.isfile(input_file):
        filename = os.path.basename(input_file)

        # run the total segmentator on the file
        print(f'\nRunning TotalSegmentator on {filename}')
        runTotalSegmentator(input_file, os.path.join(output_path, filename))

        # calculate the dice score
        if seg_path:
            print(f'\nCalculating DICE score for {filename}')
            print(f'Using {seg_path}')
            dice = calculateDICEScore(os.path.join(output_path, filename), seg_path)

    # check if input is a directory
    elif os.path.isdir(input_file):
        count = 0
        ts_time = 0
        total_time = 0
        # open a new csv file to save the input file, segmentation file and the dice score
        if seg_path:
            seg_time = 0
            with open('temp/dice_scores.csv', 'w') as f:
                f.write('File-No, Input File, Segmentation File, Dice Score\n')

        # loop through all the files in the input directory
        for file in sorted(os.listdir(input_file)):
            try:
                # check if the file is a nifti file
                if file.endswith('.nii') or file.endswith('.nii.gz'):
                    t0 = time.time()
                    # run the total segmentator on the file
                    print(f'\nRunning TotalSegmentator on {file}')
                    ts_start = time.time()
                    runTotalSegmentator(os.path.join(input_file, file), os.path.join(output_path, file))
                    ts_time += time.time() - ts_start

                    if seg_path:
                        # get the file number from the file name
                        file_no = int(''.join(filter(str.isdigit, file)))
                        seg_file = f'segmentation-{file_no}.nii'
                        print(f'\nCalculating DICE score for {file}')
                        print(f'Using {seg_file}')

                        # calculate the dice score
                        seg_start = time.time()
                        dice = calculateDICEScore(os.path.join(output_path, file), os.path.join(seg_path, f'segmentation-{file_no}.nii'))
                        seg_time += time.time() - seg_start

                        # write the input file, segmentation file and the dice score to the csv file
                        with open('temp/dice_scores.csv', 'a') as f:
                            f.write(f'{file_no}, {file}, {seg_file}, {dice}\n')
                    count += 1
                    total_time += time.time() - t0
            except Exception as e:
                print(f'Error processing {file}: {e}')

        print(f'Processed {count} files')
        print(f'\nTotalSegmentator time: {ts_time} seconds')
        print(f'Average TotalSegmentator time per file: {ts_time/count} seconds')
        if seg_path:
            print(f'Segmentation time: {seg_time} seconds')
            print(f'Average Segmentation time per file: {seg_time/count} seconds')
        print(f'\nTotal time: {total_time} seconds')
        print(f'Average time per file: {total_time/count} seconds')

if __name__ == '__main__':
    main()