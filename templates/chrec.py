# import the necessary packages
import cv2

class CharactersRecognition:
    def __init__(self, debug=False):
        self.debug = debug

    #OPTIONAL
    def debug_imshow(self, title, image, waitKey=False):
        if self.debug:
            cv2.imshow(title, image)

            if waitKey:
                cv2.waitKey(0)

    def recognize(self, lp):
        return lpText