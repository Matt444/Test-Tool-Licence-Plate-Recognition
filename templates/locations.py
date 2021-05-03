from xml.dom import minidom
import xml.etree.ElementTree as ET

def get(image_name):
    res = []
    info_file = minidom.parse(image_name + '.xml')
    i = 0
    while 1:
        try:
            xmin = int(info_file.getElementsByTagName("xmin")[i].firstChild.data)
            ymin = int(info_file.getElementsByTagName("ymin")[i].firstChild.data)
            xmax = int(info_file.getElementsByTagName("xmax")[i].firstChild.data)
            ymax = int(info_file.getElementsByTagName("ymax")[i].firstChild.data)
            res.append((xmin, ymin, xmax, ymax))
            i += 1
        except:
            break

    return res