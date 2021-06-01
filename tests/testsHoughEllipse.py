import envtest
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
from skimage.data import coffee

class TestHoughEllipse(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testCoffee(self):
        image = coffee()
        self.assertIsNotNone(image)
        # plt.imshow(image)
        # plt.show()

    def testCropCoffee(self):
        image = coffee()[0:220, 160:420]
        self.assertIsNotNone(image)
        # plt.imshow(image)
        # plt.show()


if __name__ == "__main__":
    envtest.main()
