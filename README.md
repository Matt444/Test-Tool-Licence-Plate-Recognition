# Test Tool for Licence Plate Recognition

usage: ttlpr.py [-h] [-i INPUT_IMAGES] [-iv INPUT_VIDEO] [-d] [-s] [-ol] [-or] [-o OUTPUT] <br>

optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -i INPUT_IMAGES, --input_images INPUT_IMAGES<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; path to input directory of images<br>
  -iv INPUT_VIDEO, --input_video INPUT_VIDEO<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;path to input video file<br>
  -d, --debug           whether or not to show additional visualizations<br>
  -s, --show_results    whether or not to show results<br>
  -ol, --only_license_plates_location<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; whether only run license plates location<br>
  -or, --only_characters_recognition<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; whether only run characters recognition<br>
  -o OUTPUT, --output OUTPUT<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; path to output directory for processed images/video<br>

## Connect your python scripts to locate and recognice car plates

File lpl.py for locate plates should consist of:
* class LicensePlatesLocator with boolean argument debug in constructor,
* function locate_license_plates(**image**) inside mentioned class with type used in cv2 library for images
* list of 2-tuples consisted of rois (part of image where license plate was found ) and rectangles (where that was found in format (x,y,w,h)) eg. [(roi1,rect1), (roi2, rect2), ... ] is returned

File chrec.py for plate recognition should consist of:
* class CharactersRecognition with boolean argument debug in constructor,
* function recognize(**roi**, **rect**) inside mentioned class where **roi** is part of image with license plate and **rect** in format (x,y,w,h)
* 2-tuple consist from text and rect eg. (text,rect) is returned

> Notice that mentioned files should be in the same directory as this script

## Examples of use:
python ttlpr.py -i license_plates/group1 --> processing given images in directory license_plates/group1

python ttlpr.py -i license_plates/group2 -ol --> processing given images only for location of plates

python ttlpr.py -i license_plates/group3 -or --> processing given images only for characters recognition

