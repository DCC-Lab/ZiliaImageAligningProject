"""Here is what I need to do:
1. Find the ONH in the picture (will most likely have a minimum brightness
and size)
2. Approximate it as an ellipse
3. Use the middle of this ellipse to determine the reference point for the
first picture, and the shift for the subsequent pictures.
4. Discard images if the ONH is not found (retina AND related rosa images).
"""

# Import image as grayscale
# Reduce image size by some factor
# Apply gamma correction to accentuate contrasts (handle IndexError!!!)
# Find Otsu's threshold
# Turn the image into a binary image according to the threshold
# Apply a canny filter
# Apply an elliptical Hough transform
# Get the best ellipse parameters for the small picture
# Convert those parameters to make them work with the big picture
# Return (or store) the ellipse parameters


import numpy as np
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.exposure import adjust_gamma


class ONHDetection:

    def __init__(self, image, scaleFactor=3, gamma=False, minMajorAxisScale=1/6, maxMinorAxisScale=0.5, accuracy=10):
        self.image = image
        self.scaleFactor = scaleFactor
        self.gamma = gamma
        self.minMajorAxisScale = minMajorAxisScale
        self.maxMinorAxisScale = maxMinorAxisScale
        self.accuracy = accuracy
        self.smallGrayImage = np.array([])
        self.grayImage = rgb2gray(image)
        self.threshold = 0
        self.smallBinaryImage = np.array([])
        self.contours = np.array([])
        self.minMajorAxis = 0
        self.maxMinorAxis = 0
        self.houghResult = None

    def getRescaledImage(self):
        outputSize = grayImage.shape[0]//self.scaleFactor, grayImage.shape[1]//self.scaleFactor
        self.smallGrayImage = resize(self.grayImage, outputSize)

    def detectGammaNecessity(self):
        # has to be coded
        pass

    def adjustGamma(self):
        # only execute if gamma is not False
        self.smallGrayImage = adjust_gamma(self.smallGrayImage, gamma=self.gamma)

    def getThreshold(self):
        self.threshold = threshold_otsu(self.smallGrayImage)

    def binarizeImage(self):
        self.smallBinaryImage = self.smallGrayImage > self.threshold

    def applyCannyFilter(self):
        self.contours = canny(self.smallBinaryImage)

    def defineONHRelativeScale(self):
        xSize = self.smallGrayImage.shape[0]
        ySize = self.smallGrayImage.shape[1]
        self.minMajorAxis = int(minMajorAxisScale*ySize)
        self.maxMinorAxis = int(maxMinorAxisScale*xSize)

    def applyHoughTransform(self):
        self.houghResult = hough_ellipse(self.contours,
                                    min_size=self.minMajorAxis,
                                    max_size=self.maxMinorAxis,
                                    accuracy=self.accuracy,
                                    threshold=self.threshold)

    def getBestEllipse(self):
        self.houghResult.sort(order='accumulator')
        self.smallScaleBestEllipse = list(self.houghResult[-1])

    def unpackAndUpscaleParameters(self):
        yc, xc, a, b = [int(round(x)*self.scaleFactor) for x in self.smallScaleBestEllipse[1:5]]
        orientation = best[5]
        self.yCenter = yc
        self.xCenter = xc
        self.minorAxis = a
        self.majorAxis = b
        self.orientation = orientation

    def returnBestEllipse(self):
        return self.xCenter, self.yCenter, self.minorAxis, self.majorAxis, self.orientation

    # Use names under??? À regarder...



    # def cleanRetinaImage(image, sigma=3):
    #     """Apply a filter (canny filter?) to clean the image before
    #     turning it into a binary image. Would have to find a good default
    #     sigma."""


    # def binarizeRetinaImage():
    #     """Turn a clean image into a binary image before applying a Hough
    #     transform."""


    # def findOpticNerveHead():
    #     """Tell if minimum brightness and circle size have been found,
    #     probably returns a bool. Maybe use the ConnectedComponents class..."""


    # def findClosestCircle():
    #     """If the ONH was found, approximate it as a circle.
    #     Probably returns the circle's center coordinates and radius."""


    # def determineShift():
    #     """Use the position of the ONH circle approximation and find how
    #     far it is from the center of the image, which will give us the shift
    #     value to apply"""
