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
from skimage import color, img_as_ubyte
from skimage.transform import resize
from skimage.exposure import adjust_gamma
import time

"""
This is a continuance of the "testsHoughEllipse" file, but this one will
only have as a goal to verify if the parameters found in the other file will
suit all the test images.
"""

class TestHoughEllipse(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def evaluateHoughEllipseWithRescale(self, fileName, accuracy=1, minMajorAxisScale=1/6, maxMinorAxisScale=0.5,
                                        threshold=4, scaleFactor=5, showSmallCanny=False, gamma=0, tellThresh=False):
        # To prevent repetition in subsequent tests.
        imageRgb = imread(self.testCannyDirectory+"/"+fileName)
        grayImage = imread(self.testCannyDirectory+"/"+fileName, as_gray=True)
        if gamma != 0:
            grayImage = adjust_gamma(grayImage, gamma=gamma)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)

        smallGrayImage = resize(grayImage, (grayImage.shape[0]//scaleFactor, grayImage.shape[1]//scaleFactor))
        if gamma != 0:
            smallGrayImage = adjust_gamma(smallGrayImage, gamma=gamma)
            plt.imshow(smallGrayImage, cmap=plt.cm.gray)
            plt.show()
        smallThresh = threshold_otsu(smallGrayImage)
        if tellThresh:
            print(smallThresh)
        smallBinaryImage = smallGrayImage > smallThresh
        smallCanniedImage = canny(smallBinaryImage)
        if showSmallCanny:
            plt.imshow(smallCanniedImage, cmap=plt.cm.gray)
            plt.show()

        xSize = smallGrayImage.shape[0]
        ySize = smallGrayImage.shape[1]
        minMajorAxis = int(minMajorAxisScale*ySize)
        maxMinorAxis = int(maxMinorAxisScale*xSize)

        houghResult = hough_ellipse(smallCanniedImage, min_size=minMajorAxis,
            max_size=maxMinorAxis, accuracy=accuracy, threshold=threshold)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        smallBest = list(houghResult[-1])
        return smallBest, imageRgb, canniedImage

    def plotHoughEllipseWithRescale(self, smallBest, imageRgb, canniedImage, scaleFactor=5):
        # To prevent repetition in subsequent tests.
        yc, xc, a, b = [int(round(x)*scaleFactor) for x in smallBest[1:5]]
        orientation = smallBest[5]
        # Draw the ellipse on the original image
        cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
        imageRgb[cy, cx] = (0, 0, 255)
        # Draw the edge (white) and the resulting ellipse (red)
        canniedImage = color.gray2rgb(img_as_ubyte(canniedImage))
        canniedImage[cy, cx] = (250, 0, 0)
        fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                        sharex=True, sharey=True)
        ax1.set_title('Original picture')
        ax1.imshow(imageRgb)
        ax2.set_title('Edge (white) and result (red)')
        ax2.imshow(canniedImage)
        plt.show()

    def testLastUsedParametersWithAllPictures(self):
        pass

    @envtest.skip("Skip plots")
    def testBresilHigh(self):
        fileName = "bresilHigh.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, gamma=3, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.5833196407833887
        # gamma3Thresh = 0.4902343751110835
        # Very good!!! Can go down to gamma = 2 with pretty good results, but
        # higher values are better.

    @envtest.skip("Skip plots")
    def testBresilMedium(self):
        fileName = "bresilMedium.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.4698714712041806
        # Works only with gamma = 1 or 0, else it raises an error or gives
        # something disgusting!!!

    @envtest.skip("Skip plots")
    def testBresilMediumLow(self):
        fileName = "bresilMedium-Low.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.28459210192751555
        # Works ok with gamma 1, but not well with gamma 2.

    @envtest.skip("Skip plots")
    def testKenyaHigh(self):
        fileName = "kenyaHigh.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=3, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.5820767615854621
        # gamma3Thresh = 0.4902343750831357
        # Works relatively well with gamma 2.5 or higher.

    @envtest.skip("Skip plots")
    def testKenyaLow(self):
        fileName = "kenyaLow.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.19683273442312746
        # Never works well (bad picture, really...), but best with 0 <= gamma <= 1.
        # WAIITTTT works much better with a scale factor of 3!!!

    @envtest.skip("Skip plots")
    def testKenyaMedium(self):
        fileName = "kenyaMedium.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.37775883053396575
        # Works well with 0 <= gamma <= 1.

    @envtest.skip("Skip plots")
    def testRwandaHigh(self):
        fileName = "rwandaHigh.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # threshGamma3 = 0.49023437508136586
        # threshGamma1 = 0.6107051260821916
        # Not too bad with gamma = 1, works best with gamma 2

    @envtest.skip("Skip plots")
    def testRwandaLow(self):
        fileName = "rwandaLow.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=0, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # scale factor of 5 looks better than 3...
        # thresh = 0.20642408546230254
        # Works pretty well with gamma between 0 and 1, not higher, though...

    @envtest.skip("Skip plots")
    def testRwandaMedium(self):
        fileName = "rwandaMedium.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.31824377972753254
        # Not very good with gamma 0-1, error for higher gammas.

    @envtest.skip("Skip plots")
    def testSomalieHigh(self):
        fileName = "somalieHigh.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=3)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # Not too terrible with gamma=0, just ok with higher gammas, but never
        # great... probably best with gamma=5.

    @envtest.skip("Skip plots")
    def testSomalieLow(self):
        fileName = "somalieLow.jpg"
        scaleFactor = 3
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.1925001766736212
        # gamma1 = BEURK
        # raises IndexError with high gamma, always disgusting, VERY LONG

    # @envtest.skip("Skip plots")
    def testSomalieMedium(self):
        fileName = "somalieMedium.jpg"
        scaleFactor = 5
        smallBest, imageRgb, canniedImage = self.evaluateHoughEllipseWithRescale(fileName, accuracy=10, scaleFactor=scaleFactor, showSmallCanny=True, gamma=1, tellThresh=True)
        self.plotHoughEllipseWithRescale(smallBest, imageRgb, canniedImage, scaleFactor=scaleFactor)
        # thresh = 0.5280446827374633
        # very good with gamma from 0-1. Disgusting with anything higher.
        # WAY BETTER with scale factor 5 (vs 3)...

if __name__ == "__main__":
    envtest.main()
