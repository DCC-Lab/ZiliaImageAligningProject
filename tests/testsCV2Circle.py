import envtest
from cv2 import circle
from cv2 import imread
import cv2
import matplotlib.pyplot as plt

class TestCV2Circle(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testTheBlackTestPictureIsReallyBlack(self):
        image = imread(self.testCV2CircleDirectory + "/" + "blackImage.jpg")
        self.assertIsNotNone(image)
        # print(image)
        self.assertFalse(image.all())
        self.assertFalse(image.any())

    def testDrawingARedCircleOnABlackPictureToKnowIfCoordinatesAreInPixels(self):
        # I have no choice to test multiple things at the same time
        # because the "circle" method has 5 mandatory input arguments.
        image = imread(self.testCV2CircleDirectory + "/" + "blackImage.jpg")
        self.assertIsNotNone(image)
        self.assertTrue(image.shape == (11,14,3))
        # print(image)
        centerCoordinates = (7, 5)
        circleRadius = 4
        circleColor = (255, 0, 0) # red in RGB
        thickness = 2
        circle(image, centerCoordinates, circleRadius, circleColor, thickness)
        self.assertTrue(image.any())
        # plt.imshow(image)
        # plt.show()
        # Yes, everything is in pixels (has been visually verified, because
        # the "circle" function has so many mandatory input arguments).
        # And yes, the original picture placed as an input argument in "circle"
        # is modified by the function even if we don't reassing it to another
        # variable.

if __name__ == "__main__":
    envtest.main()
