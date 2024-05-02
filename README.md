# Total Segmentator Dice Score Utility for Liver

This utility script helps you perform segmentation on NIFTI files containing full body CT-scans using TotalSegmentator.
Optionally, if the ground truth segmentations are provided then it can also calculate the Dice similarity coefficient (DICE score) to evaluate the performance of the segmentation. 
TotalSegmentator is a state-of-the-art tool for automatic segmentation of anatomical structures in medical images, and the Dice score is a common metric for assessing the quality of image segmentations.

## Installation

1. First, ensure you have Python3.9+ installed on your system. If not, download and install it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries using pip:

```sh
pip install -r requirements.txt
```

## Usage

The script can be used in two modes: single file mode and directory mode.

### Single File Mode

To process a single NIfTI file and calculate the Dice score against a provided segmentation:

```sh
python3 src/liverSegmentationTotalSegmentator.py <input_file.nii> <ground_truth_segmentation.nii>[OPTIONAL]
```

Replace `<input_file.nii>` with the path to the NIfTI file you wish to segment, and `<ground_truth_segmentation.nii>` with the path to the ground-truth segmentation file for calculating the Dice score.

### Directory Mode

You can also supply a directory containing multiple NIfTI files to process them in bulk:

```sh
python3 src/liverSegmentationTotalSegmentator.py <input_directory> <ground_truth_directory>[OPTIONAL]
```

If you just want to get the TotalSegmentator output and don't have ground truth segmentations to compare dice scores, simply omit the last argument in the python3 command.

Ensure `<input_directory>` contains the NIfTI files to be segmented, and `<ground_truth_directory>` contains the corresponding ground-truth segmentation files in NIfTI format named in correspondence with the input files for calculating the Dice scores.

## Output

The script creates a temporary directory named `temp/` to store the segmentation outputs produced by TotalSegmentator. Additionally, if operating in directory mode and have provided the ground truth segmentations, the script creates a `dice_scores.csv` file in the `temp/` directory that lists the file names, segmentation files, and the calculated Dice scores.

## Note

- The Dice score is a statistical measure that ranges from 0 to 1, where 1 indicates perfect and complete overlap.
- Modify the script as necessary for specific segmentation labels and evaluation needs.
- This uses TotalSegmentator v2 which has improved performances for segmentation output.
- Change the TotalSegmentator arguments as required.

## License

This script is distributed under the MIT license. Feel free to modify, distribute, or contribute to it. However, please note that the TotalSegmentator tool might have its own licensing that you need to comply with.