# USAGE
# python test_license_plate_recognition.py -i license_plates/group1

import time
import importlib
from imutils import paths
import argparse
import imutils
import cv2
import sys
import os
from lpl import LicensePlatesLocator
from chrec import CharactersRecognition

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_images", required=False,
	help="path to input directory of images")
ap.add_argument("-iv", "--input_video",
	help="path to input video file")
ap.add_argument("-d", "--debug", action="store_true", default=False,
	help="whether or not to show additional visualizations")
ap.add_argument("-s", "--show_results", action="store_true", default=False,
	help="whether or not to show results")
ap.add_argument("-ol","--only_license_plates_location", action="store_true", default=False,
	help="whether only run license plates location")
ap.add_argument("-or", "--only_characters_recognition", action="store_true", default=False,
	help="whether only run characters recognition")
ap.add_argument("-o", "--output", required=False,
	help="path to output directory for processed images/video")
args = vars(ap.parse_args())

lpl = LicensePlatesLocator(debug=args["debug"] > 0)
chrec = CharactersRecognition(debug=args["debug"] > 0)
location_time = 0
recognition_time = 0
recognized_plates = 0
images_processed = 0
images_to_process = 1


def process_image(gray):
	global args, location_time, recognition_time, recognized_plates, images_processed, images_to_process
	#progress(images_processed/images_to_process * 100)
	sys.stdout.write("\rProcessing: %i" % (images_processed + 1))
	sys.stdout.write("/%i" % images_to_process)
	sys.stdout.write(" --> %0.2f" % round((images_processed+1)/images_to_process * 100,2))
	sys.stdout.write("%")
	sys.stdout.flush()

	rois = []
	if(args["only_characters_recognition"]):
		h, w = gray.shape
		rois.append((gray, (0,0,w,h)))
	else:
		timer = time.time()
		rois = lpl.locate_license_plates(gray)
		location_time += (time.time() - timer)
		if (args["output"]):
			dir = args["output"] + "/found_plates/"
			if not os.path.exists(dir):
				os.makedirs(dir)
			i = 1
			for (roi, rect) in rois:
				cv2.imwrite(dir + str(images_processed+1) + "_" + str(i) + ".jpg", roi)
				i += 1

	if (args["only_license_plates_location"] == False):
		if_some_plate_were_detected = 0
		i = 1
		for (roi, rect) in rois:
			timer = time.time()
			(lpText, rect) = chrec.recognize(roi, rect)
			recognition_time += (time.time() - timer)

			# only continue if the license plate was successfully recognized
			if lpText is not None and rect is not None:
				recognized_plates += 1
				if_some_plate_were_detected = 1

				(x, y, w, h) = rect

				cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
				cv2.putText(image, cleanup_text(lpText), (x, y - 15),
							cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

				if (args["show_results"]):
					print("[INFO] {}".format(lpText))

				if (args["output"]):
					dir = args["output"] + "/recognized_plates/"
					if not os.path.exists(dir):
						os.makedirs(dir)
					cv2.imwrite(dir + str(images_processed + 1) + "_" + str(i) + ".jpg", image)
					i += 1

		if (args["output"]):
			outVideo.write(image)

		if (args["show_results"] and if_some_plate_were_detected):
			cv2.imshow("Processed Image", image)
			cv2.waitKey(0)

	images_processed += 1


all_process_time = time.time()

if (args["input_images"]):
	imagePaths = sorted(list(paths.list_images(args["input_images"])))
	images_to_process =  len(imagePaths)

	for imagePath in imagePaths:
		image = cv2.imread(imagePath)
		if(args["only_characters_recognition"] == False):
			image = imutils.resize(image, width=600)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		process_image(gray)


elif(args["input_video"]):
	video = cv2.VideoCapture(args["input_video"])
	if(args["output"] and video.isOpened()):
		frame_width = int(video.get(3))
		frame_height = int(video.get(4))
		fps = video.get(cv2.CAP_PROP_FPS)
		outVideo = cv2.VideoWriter(args["output"] + '/processed_vid.mp4',0x7634706d, fps, (frame_width,frame_height))
	images_to_process = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

	#startProgress("Processing video")
	while (video.isOpened()):
		ret, image = video.read()
		if ret == False:
			break

		#if(args["only_characters_recognition"] == False):
		#	image = imutils.resize(image, width=600)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		process_image(gray)

	video.release()
	cv2.destroyAllWindows()

if(args["input_images"] or args["input_video"]):
	print("\n---------------SUMMARY---------------")
	print("Processed images:", images_processed)
	print("Recognized plates:", recognized_plates)
	location_time = round(location_time * 1000)
	recognition_time = round(recognition_time * 1000)
	all_process_time = round((time.time() - all_process_time) * 1000)
	print("----------------TIMERS----------------")
	print("Location time:", location_time, "ms")
	print("Recognition time:", recognition_time, "ms")
	print("All process time:", all_process_time, "ms")
	print("Time for image:", all_process_time/images_processed, "ms")
	print(round((images_processed/all_process_time)*1000,2), "images/s")

else:
	print("No input data, run program with -h flag to get to know how to select data")


