from ziliaImage.affinetransform import AffineTransform
import sqlite3 as lite
import cv2
import numpy as np


class ImageAlignment:
    def __init__(self, reference):
        if type(reference) == np.ndarray:
            self.ref = reference
        else:
            self.ref = self.readImage(reference)
        self.regImg = None
        self.traImg = None
        self.srReference = None

    def readImage(self, path: str):
        try:
            return cv2.imread(path, cv2.COLOR_BGR2GRAY)
        except:
            raise TypeError('Image cannot converted into a numpy array. Expected a string type path, got a {}'.format(type(path)))

    def imgToTransform(self, image):
        if type(image) == np.ndarray:
            self.traImg = image
        else:
            self.traImg = self.readImage(image)

    def imgToRegister(self, image):
        if type(image) == np.ndarray:
            self.regImg = image
        else:
            self.regImg = self.readImage(image)

    def readImagePair(self, pair: list):
        return self.readImage(pair[0]), self.readImage(pair[1])

    def initiateSRReference(self):
        # Dimensions of the image are modified to ignore some artefacts on the sides.
        # Default is 180:2250, 160:1860, 2
        self.srReference = AffineTransform(self.ref[180:2250, 160:1860, 2])

    def setRegistration(self):
        # Dimensions of the image are modified to ignore some artefacts on the sides.
        # Default is 180:2250, 160:1860, 2
        self.srReference.register(self.regImg[180:2250, 160:1860, 2])

    def transform(self, chan=None):
        newImg = np.zeros(self.ref.shape, dtype=int)
        if chan is None:
            for channel in range(self.ref.shape[2]):
                newImg[:, :, channel] = self.srReference.transform(self.traImg[:, :, channel])
        else:
            newImg[:, :, chan] = self.srReference.transform(self.traImg[:, :, chan])

        self.traImg = newImg.astype(np.uint8)
        return self.traImg

    def registerAndTransform(self):
        self.setRegistration()
        return self.transform()
