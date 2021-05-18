from affinetransform import AffineTransform
import cv2
import numpy as np


class ImageAlignment:
    def __init__(self, reference):
        if type(reference) == np.ndarray:
            self.ref = reference
        else:
            self.ref = cv2.imread(reference)
        self.img = None
        self.srReference = None

    def readImage(self, path: str):
        self.img = cv2.imread(path)

    def initiateSRReference(self):
        # Dimensions of the image are modified to ignore some artefacts on the sides.
        self.srReference = AffineTransform(self.ref[180:2250, 160:1860, 2])

    def setRegistration(self):
        # Dimensions of the image are modified to ignore some artefacts on the sides.
        self.srReference.register(self.img[180:2250, 160:1860, 2])

    def transform(self, chan=None):
        newImg = np.zeros(self.ref.shape, dtype=int)
        if chan is None:
            for channel in range(self.ref.shape[2]):
                newImg[:, :, channel] = self.srReference.transform(self.img[:, :, channel])
        else:
            newImg[:, :, chan] = self.srReference.transform(self.img[:, :, chan])

        self.img = newImg.astype(np.uint8)
        return self.img
