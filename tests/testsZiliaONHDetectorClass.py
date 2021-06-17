import envtest
from analyzeRetinaImages import *
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.color import rgb2gray, gray2rgb
from skimage import img_as_ubyte
from skimage.draw import ellipse_perimeter

class TestZiliaONHDetectorClass(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportImage(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        self.assertIsNotNone(image)

    def testCreateDetectorColorImage(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        detector = ZiliaONHDetector(image)
        self.assertIsNotNone(detector)
        # print(type(detector))

    def testCreateDetectorGrayImage(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        grayImage = rgb2gray(image)
        detector = ZiliaONHDetector(grayImage)
        self.assertIsNotNone(detector)

    def testGetParamsCorrections(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        detector = ZiliaONHDetector(image)
        detector.getParamsCorrections()
        self.assertIsNotNone(detector)

    @envtest.skip("skip plot")
    def testPreProcessImage(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        detector = ZiliaONHDetector(image)
        detector.getParamsCorrections()
        detector.preProcessImage()
        self.assertIsNotNone(detector)
        plt.imshow(detector.contours, cmap="gray")
        plt.show()
        self.assertIsNotNone(detector)

    def plotHoughEllipseWithRescale(self, result, imageRgb, canniedImage):
        # To prevent repetition in subsequent tests.
        (xCenter, yCenter), minorAxis, majorAxis, orientation = result
        # Draw the ellipse on the original image
        cy, cx = ellipse_perimeter(yCenter, xCenter, minorAxis, majorAxis, orientation)
        imageRgb[cy, cx] = 130
        # Draw the edge (white) and the resulting ellipse (red)
        canniedImage = gray2rgb(img_as_ubyte(canniedImage))
        canniedImage[cy, cx] = (250, 0, 0)
        fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                        sharex=True, sharey=True)
        ax1.set_title('Original picture')
        ax1.imshow(imageRgb)
        ax2.set_title('Edge (white) and result (red)')
        ax2.imshow(canniedImage)
        plt.show()

    @envtest.skip("skip plot")
    def testFindONH(self):
        image = imread(self.testCannyDirectory+"/bresilMedium.jpg")
        detector = ZiliaONHDetector(image)
        detector.getParamsCorrections()
        detector.preProcessImage()
        result = detector.findOpticNerveHead()
        self.plotHoughEllipseWithRescale(result, image, image)

if __name__ == '__main__':
    envtest.main()
