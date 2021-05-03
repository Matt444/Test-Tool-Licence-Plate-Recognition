import os
import cv2
from xml.dom import minidom
from xml.etree import ElementTree
import xml.etree.ElementTree as ET

def save_license_location_annotations(location, image_name, rois, numbers):
    annotations = location + "/annotations/"
    if not os.path.exists(annotations):
        os.makedirs(annotations)

    root = ET.Element("results")
    tree = ET.ElementTree()

    i = 0
    for (roi, rect) in rois:
        data = ET.Element('plate')
        (x, y, w, h) = rect

        ET.SubElement(data, 'xmin').text = str(x)
        ET.SubElement(data, 'ymin').text = str(y)
        ET.SubElement(data, 'xmax').text = str(x + w)
        ET.SubElement(data, 'ymax').text = str(y + h)
        if numbers[i] == '':
            numbers[i] = '-'
        ET.SubElement(data, 'numbers').text = str(numbers[i])

        # create a new XML file with the results
        root.append(data)
        i += 1

    tree._setroot(root)
    tree.write(annotations + image_name + '.xml')

def save_found_plates(location, image_nr, rois):
    dir = location + "/found_plates/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    i = 1
    for (roi, rect) in rois:
        cv2.imwrite(dir + str(image_nr) + "_" + str(i) + ".jpg", roi)
        i += 1

def save_result_of_license_recognition(location, image_name, image):
    dir = location + "/recognized_plates/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    cv2.imwrite(dir + image_name + ".jpg", image)