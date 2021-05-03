# import the necessary packages
import cv2

class LicensePlatesLocator:
    def __init__(self, debug=False):
        self.debug = debug

    #OPTIONAL
    def debug_imshow(self, title, image, waitKey=False):
        if self.debug:
            cv2.imshow(title, image)

            if waitKey:
                cv2.waitKey(0)

    def locate_license_plates(self, gray):
        candidates = [(0,0,10,10)] #[(xmin,ymin,w,h)]
        return candidates

