import argparse

def define(ap):
    ap.add_argument("-i", "--input_images", required=False,
                    help="path to input directory of images")
    ap.add_argument("-iv", "--input_video",
                    help="path to input video file")
    ap.add_argument("-d", "--debug", action="store_true", default=False,
                    help="whether or not to show additional visualizations")
    ap.add_argument("-s", "--show_results", action="store_true", default=False,
                    help="whether or not to show results")
    ap.add_argument("-ol", "--only_license_plates_location", action="store_true", default=False,
                    help="whether only run license plates location")
    ap.add_argument("-or", "--only_characters_recognition", action="store_true", default=False,
                    help="whether only run characters recognition")
    ap.add_argument("-o", "--output", required=False,
                    help="path to output directory for processed images/video")
    ap.add_argument("-vl", "--verify_locations",
                    help="path to locations.py file which returns location of plate of given image_name in format (xmin, ymin, xmax, ymax) is required")
    ap.add_argument("-vr", "--verify_characters_recognition",
                    help="path to values.py file which returns value of plate of given image_name is required")
