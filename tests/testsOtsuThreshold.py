import envtest
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np

class TestThreshAndBinary(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportTestImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        self.assertIsNotNone(image)

    def testImportGrayscaleImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = rgb2gray(image)
        self.assertIsNotNone(grayImage)

    def testOtsuThreshColorImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        thresh = threshold_otsu(image)
        self.assertIsNotNone(thresh)

    def testTypeOtsuThreshColorImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        thresh = threshold_otsu(image)
        # print(type(thresh))
        self.assertTrue(type(thresh) == np.int32)

    def testOtsuThreshGrayscaleImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        self.assertIsNotNone(thresh)

    def testTypeOtsuThreshGrayscaleImage(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        # print(type(thresh))
        self.assertTrue(type(thresh) == np.float64)

    def testBinarizeGrayImageWithOtsu(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertIsNotNone(binaryImage)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()

    def testTypeOfBinaryImageElements(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertTrue(binaryImage.dtype == np.bool_)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()

    def testBinarizeColorImageWithOtsu(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        self.assertIsNotNone(binaryImage)
        # Can't run the 2 lines below to show the result...
        # so it seems like turning the image to grayscale is mandatory
        # before thresholding.
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()

    def testLowLightImageThresh1(self):
        image = imread(self.testCannyDirectory+"/somalieLow.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # not great, but the image is very bad...

    def testLowLightImageThresh2(self):
        image = imread(self.testCannyDirectory+"/kenyaLow.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # GREAT!!!

    def testMidLightImageThresh1(self):
        image = imread(self.testCannyDirectory+"/rwandaMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Good!

    def testMidLightImageThresh2(self):
        image = imread(self.testCannyDirectory+"/somalieMedium.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Good!

    def testHighLightImageThresh1(self):
        image = imread(self.testCannyDirectory+"/bresilHigh.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # NOT GOOD, sees too much things as the blob, but the image is very
        # washed out...

    def testHighLightImageThresh2(self):
        image = imread(self.testCannyDirectory+"/rwandaHigh.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Not too bad, but not that great...

    def testHighLightImageThresh3(self):
        image = imread(self.testCannyDirectory+"/somalieHigh.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Pretty good :)

    @envtest.skip("Skip plots")
    def testHighLightImageThresh4(self):
        image = imread(self.testCannyDirectory+"/kenyaHigh.jpg")
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        plt.imshow(binaryImage, cmap=plt.cm.gray)
        plt.show()
        # Very bad, picture far from optimal, though...

if __name__ == "__main__":
    envtest.main()
