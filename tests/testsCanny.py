import envtest
from skimage.io import imread
from skimage.feature import canny
from skimage.color import rgb2gray
from processImages import *

class TestCanny(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportTestImage(self):
        image = imread(self.testCannyDirectory+"/cannyTest.jpg")
        self.assertIsNotNone(image)

    def testRGB2Gray(self):
        image = imread(self.testCannyDirectory+"/cannyTest.jpg")
        self.assertTrue(image.shape[2] == 3)
        grayImage = rgb2gray(image)
        self.assertIsNotNone(grayImage)
        self.assertTrue(len(grayImage.shape) == 2)
        # processedImage = canny(image)
        # self.assertIsNotNone(processedImage)


if __name__ == "__main__":
    envtest.main()
