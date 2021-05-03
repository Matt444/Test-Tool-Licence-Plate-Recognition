# USAGE
# python test_license_plate_recognition.py -i license_plates/group1

import time
import argparse
import imutils
import cv2
import sys
import os
from imutils import paths

from lpl import LicensePlatesLocator
from chrec import CharactersRecognition
from app.lprs import LicensePlatesRecognitionStats
from app import results, validator, argparser

def cleanup_text(text):
	return "".join([c if 64 < ord(c) < 91 or 48 < ord(c) < 58 else "" for c in text]).strip()

ap = argparse.ArgumentParser()
argparser.define(ap)
args = vars(ap.parse_args())

lpl = LicensePlatesLocator(debug=args["debug"] > 0)
chrec = CharactersRecognition(debug=args["debug"] > 0)
stats = LicensePlatesRecognitionStats()

def process_image(image, lpl, chrec, args, stats):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	sys.stdout.write("\rProcessing: %i" % (stats.images_processed + 1))
	sys.stdout.write("/%i" % stats.images_to_process)
	sys.stdout.write(" --> %0.2f" % round((stats.images_processed + 1)/stats.images_to_process * 100, 2))
	sys.stdout.write("%")
	sys.stdout.flush()

	rois = [] #shortcut from regions of interest
	if args["only_characters_recognition"]:
		h, w = gray.shape
		rois.append((gray, (0, 0, w, h)))
	else:
		timer = time.time()
		rois = lpl.locate_license_plates(gray)
		stats.location_time += (time.time() - timer)

		if args["output"]:
			results.save_found_plates(args["output"], stats.images_processed + 1, rois)

	values = []
	for (roi, rect) in rois:
		(x, y, w, h) = rect
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		lpText = ''
		if args["only_license_plates_location"] == False:
			timer = time.time()
			lpText = chrec.recognize(roi)
			stats.recognition_time += (time.time() - timer)

			if lpText is not None:
				cv2.putText(image, cleanup_text(lpText), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

				if args["show_results"]:
					print("\n[INFO] {}".format(cleanup_text(lpText)))

		values.append(cleanup_text(lpText))

	if args["output"]:
		results.save_result_of_license_recognition(args["output"], str(stats.images_processed + 1), image)
		if args["input_images"]:
			results.save_license_location_annotations(args["output"], image_name, rois, values)
		if args["input_video"]:
			outVideo.write(image)

	stats.found_plates += len(rois)
	if args["verify_locations"] or args["verify_characters_recognition"] and len(rois) > 0:
		(all_plates, correctly_detected, sum_rec_accuracy) = validator.verify_found_locations_and_values(
			args["verify_locations"], args["verify_characters_recognition"], image_name, rois, values, args['show_results'])
		stats.all_plates += all_plates
		stats.correctly_found_plates += correctly_detected
		stats.average_recognition_accuracy += sum_rec_accuracy

	if args["show_results"]:
		cv2.imshow("Processed Image", image)
		cv2.waitKey(0)

	stats.images_processed += 1



if args["input_images"]:
	imagePaths = sorted(list(paths.list_images(args["input_images"])))
	stats.images_to_process =  len(imagePaths)

	for imagePath in imagePaths:
		image_name = imagePath.split("\\")[-1].split('.')[0]
		image = cv2.imread(imagePath)
		if(args["only_characters_recognition"] == False):
			image = imutils.resize(image, width=600)

		process_image(image, lpl, chrec, args, stats)


elif args["input_video"]:
	video = cv2.VideoCapture(args["input_video"])
	if(args["output"] and video.isOpened()):
		frame_width = int(video.get(3))
		frame_height = int(video.get(4))
		fps = video.get(cv2.CAP_PROP_FPS)
		outVideo = cv2.VideoWriter(args["output"] + '/processed_vid.mp4',0x7634706d, fps, (frame_width, frame_height))
	stats.images_to_process = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

	while (video.isOpened()):
		ret, image = video.read()
		if ret == False:
			break
		#if(args["only_characters_recognition"] == False):
		#	image = imutils.resize(image, width=600)
		process_image(image, lpl, chrec, args, stats)

	video.release()
	cv2.destroyAllWindows()


if(args["input_images"] or args["input_video"]):
	stats.show(args)
else:
	print("No input data, run program with -h flag to get to know how to select data")


