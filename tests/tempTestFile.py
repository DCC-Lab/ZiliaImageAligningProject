import envtest
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
from skimage.data import coffee
from skimage.draw import ellipse_perimeter
from skimage.transform import hough_ellipse
from skimage.feature import canny

class TestHoughEllipse(envtest.ZiliaTestCase):

    def testHoughEllipseWithChosenEllipseParameters(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        xSize = grayImage.shape[0]
        ySize = grayImage.shape[1]
        minMajorAxis = int((1/6)*ySize)
        maxMinorAxis = int(0.5*xSize)
        houghResults = hough_ellipse(canniedImage, min_size=minMajorAxis, max_size=maxMinorAxis)
        # plt.imshow(cannied, cmap=plt.cm.gray)
        # plt.show()
        # houghResults.sort(order="accumulator")

if __name__ == "__main__":
    envtest.main()
