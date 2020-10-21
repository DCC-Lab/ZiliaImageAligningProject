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
        # Reference is the red channel of the image.
        self.srReference = AffineTransform(self.ref[90:1125, 80:930, 2])

    def setRegistration(self):
        self.srReference.register(self.img[90:1125, 80:930, 2])

    def transform(self, chan=None):
        newImg = np.zeros(self.ref.shape, dtype=int)
        if chan is None:
            for channel in range(self.ref.shape[2]):
                newImg[:, :, channel] = self.srReference.transform(self.img[:, :, channel])
        else:
            newImg[:, :, chan] = self.srReference.transform(self.img[:, :, chan])

        self.img = newImg.astype(np.uint8)
