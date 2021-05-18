from pystackreg import StackReg
import numpy as np


class AffineTransform:
    def __init__(self, reference: np.ndarray):
        self.ref = reference
        self.stackReg = StackReg(StackReg.AFFINE)

        self.registration = None
        self.transformedImage = None

    def registerAndTransform(self, image: np.ndarray):
        self.transformedImage = self.stackReg.register_transform(self.ref, image)
        return self.transformedImage

    def register(self, image: np.ndarray):
        self.registration = self.stackReg.register(self.ref, image)

    def transform(self, image: np.ndarray):
        self.transformedImage = self.stackReg.transform(image)
        return self.transformedImage