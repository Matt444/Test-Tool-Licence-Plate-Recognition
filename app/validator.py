import importlib
from fuzzywuzzy import fuzz
from xml.dom import minidom
import xml.etree.ElementTree as ET

limit_in = -10
limit_out = 15

def verify_found_locations_and_values(locations_path, values_path, image_name, rois, values, show):
    (all_plates, correctly_detected, reco_accuracy) = (0,0,0)
    if locations_path is not None:
        locations_file = importlib.import_module(locations_path.replace('\\', '.').replace('/', '.') + '.locations')
        correct_locations = locations_file.get(locations_path + '/' + image_name)
        all_plates = len(correct_locations)

    if values_path is not None:
        values_file = importlib.import_module(values_path.replace('\\', '.').replace('/', '.') + '.values')
        correct_values = values_file.get(values_path + '/' + image_name)

    i = 0
    for (roi, rect) in rois:
        (x, y, w, h) = rect
        (xmin, ymin, xmax, ymax) = (x, y, x+w, y+h)

        if locations_path is not None:
            j = 0
            for location in correct_locations:
                (cxmin, cymin, cxmax, cymax) = location
                if show:
                    print("\nFound location: xmin " + str(xmin) + " ymin " + str(ymin) + " xmax " + str(xmax) + "ymax " + str(ymax))
                    print("\nCorrr location: xmin " + str(cxmin) + " ymin " + str(cymin) + " xmax " + str(cxmax) + "ymax " + str(cymax))

                if  (limit_in < cxmin - xmin < limit_out and
                    limit_in < ymin - cymin < limit_out and
                    limit_in < cxmax - xmax < limit_out and
                    limit_in < cymax - ymax < limit_out):

                    correctly_detected += 1
                    if values_path is not None:
                        reco_accuracy += fuzz.ratio(values[i], correct_values[j])
                        if show:
                            print('\naccuracy:', reco_accuracy)
                    # if values[i] == correct_values[i]:
                    #     correctly_recognized += 1
                j += 1
        else:
            reco_accuracy += fuzz.ratio(values[i], correct_values[0])
            if show:
                print('\naccuracy:', reco_accuracy)

        i += 1


    return (all_plates, correctly_detected, reco_accuracy)
