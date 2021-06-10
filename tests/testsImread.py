import envtest
from cv2 import circle
import cv2
from skimage.io import imread as skimread
from processImages import *


class TestImread(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportImageWithSkimage(self):
        testImage = skimread(self.testSmallFilesDirectory+"/testIm.jpg")
        self.assertIsNotNone(testImage)

    def testImportImageWithCV2(self):
        testImage = cv2.imread(self.testSmallFilesDirectory+"/testIm.jpg")
        self.assertIsNotNone(testImage)

    def testSkimageReturnsNumpyArray(self):
        skImage = skimread(self.testSmallFilesDirectory+"/testIm.jpg")
        self.assertIsNotNone(skImage)
        self.assertTrue(type(skImage) == np.ndarray)
        # self.assertTrue(type(cv2Image) == np.ndarray)

    def testCV2ReturnsNumpyArray(self):
        cv2Image = cv2.imread(self.testSmallFilesDirectory+"/testIm.jpg")
        self.assertIsNotNone(cv2Image)
        self.assertTrue(type(cv2Image) == np.ndarray)
        # self.assertTrue(type(cv2Image) == np.ndarray)

    def testCV2AndSkimageDoNotReturnSameImage(self):
        skImage = skimread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(skImage)
        cv2Image = cv2.imread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(cv2Image)
        equality = np.equal(skImage, cv2Image)
        self.assertFalse(equality.all())

    def testCV2AndSkimageSecondColorChannelAreEqual(self):
        CV2Image = cv2.imread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(CV2Image)
        Skimage = skimread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(Skimage)
        cv2color2 = CV2Image[:,:,1]
        SkColor2 = Skimage[:,:,1]
        color2Equality = np.equal(cv2color2, SkColor2)
        self.assertTrue(color2Equality.all())
        # Both middle color channels are equal

    def testCV2FirstColorEqualsSkimageThirdColor(self):
        CV2Image = cv2.imread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(CV2Image)
        Skimage = skimread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(Skimage)
        cv2color1 = CV2Image[:,:,0]
        SkColor3 = Skimage[:,:,2]
        colorEquality = np.equal(cv2color1, SkColor3)
        self.assertTrue(colorEquality.all())

    def testCV2ThirdColorEqualsSkimageFirstColor(self):
        CV2Image = cv2.imread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(CV2Image)
        Skimage = skimread(self.testCV2CircleDirectory+"/testIm.jpg")
        self.assertIsNotNone(Skimage)
        cv2color3 = CV2Image[:,:,2]
        SkColor1 = Skimage[:,:,0]
        colorEquality = np.equal(cv2color3, SkColor1)
        self.assertTrue(colorEquality.all())


# so, cv2 imports as BGR and skimage as RGB...


if __name__ == "__main__":
    envtest.main()
