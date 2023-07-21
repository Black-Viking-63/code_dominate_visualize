import cv2
import dlib
#from helpers import convert_and_trim_bb
import argparse
import imutils
import time
import numpy as np

class FaceDetector:
    def __init__(self):
        # load dlib's CNN face detector
        self.detector = dlib.cnn_face_detection_model_v1(
            "/home/julianir/Julia/NIR/models/mmod_human_face_detector.dat")

    def __convert_and_trim_bb(self, image, rect):
        """
        Convetring dlib style to opnecv style bounding box 
        and trim coordinates that fall outside the images's range.
        """
        # extract the starting and ending (x, y)-coordinates of the
        # bounding box
        sp = 25
        startX = rect.left() - sp
        startY = rect.top() - sp
        endX = rect.right() + sp
        endY = rect.bottom() + sp

        # ensure the bounding box coordinates fall within the spatial
        # dimensions of the image
        startX = max(0, startX)
        startY = max(0, startY)
        endX = min(endX, image.shape[1])
        endY = min(endY, image.shape[0])

        # compute the width and height of the bounding box
        w = endX - startX
        h = endY - startY

        # return our bounding box coordinates
        return (startX, startY, w, h)

    #@yappi.profile(clock_type='wall', profile_builtins=False)
    def detect(self, image):
        #cam = cv2.VideoCapture(src)
        #
        # dispW = 320
        # dispH = 240
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

        #ret, image = src.read()

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # perform face detection using dlib's face detector
        results = self.detector(rgb, 0)
        
        # convert the resulting dlib rectangle objects to bounding boxes,
        # then ensure the bounding boxes are all within the bounds of the nput image
        boxes = [self.__convert_and_trim_bb(image, r.rect) for r in results]
        
        return boxes
        
        

     