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

    def testGrayscaleCoffee(self):
        image = coffee()
        grayImage = rgb2gray(image)
        self.assertIsNotNone(grayImage)
        # plt.imshow(grayImage, cmap=plt.cm.gray)
        # plt.show()

    def testOtsuThreshOnCoffee(self):
        image = coffee()
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertIsNotNone(binaryImage)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Pretty bad, might not be a good reference for what we want to do
        # because there are much more color intensitites than in the
        # retina images...

    def testImreadGrayscaleOption(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        self.assertIsNotNone(grayImage)
        self.assertTrue(len(grayImage.shape) == 2)

    def testDifferentGrayscaleMethods(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage1 = rgb2gray(image)
        grayImage2 = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        equality = np.equal(grayImage1, grayImage2)
        self.assertTrue(equality.all())

    def testOtsuThreshOnMidLightRetina(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertIsNotNone(binaryImage)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()

    def testOtsuThreshAndCanntOnMidLightRetina(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        self.assertIsNotNone(canniedImage)
        # plt.imshow(canniedImage, cmap=plt.cm.gray)
        # plt.show()
        # Very good :)

    @envtest.skip("Way too long, I'll change default parameters to optimize.")
    def testHoughEllipseDefaultParameters(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        cannied = canny(binaryImage)
        houghResults = hough_ellipse(cannied)
        # plt.imshow(cannied, cmap=plt.cm.gray)
        # plt.show()
        # houghResults.sort(order="accumulator")

    def testImageShape(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        shape = grayImage.shape
        self.assertIsNotNone(shape)
        self.assertTrue(len(shape) == 2)
        self.assertTrue(shape[0] < shape[1])
        # So the first dimension is the height,
        # and the second one is the width.

    @envtest.skip("Still too long, but about 60 seconds shorter than without ellipse parameter!")
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

if __name__ == "__main__":
    envtest.main()
