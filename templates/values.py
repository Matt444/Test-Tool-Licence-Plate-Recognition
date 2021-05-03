from xml.dom import minidom
import xml.etree.ElementTree as ET

def get(image_name):
    res = []
    info_file = minidom.parse(image_name + '.xml')
    i = 0
    while 1:
        try:
            numbers = str(info_file.getElementsByTagName("numbers")[i].firstChild.data)
            res.append(numbers)
            i += 1
        except:
            break

    return res