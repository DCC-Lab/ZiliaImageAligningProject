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


class EllipseDetector:
    # To be coded later
    pass


class ZiliaONHDetector(EllipseDetector):

    def __init__(self, image, scaleFactor=3, gamma=True, relativeMinMajorAxis=1/6, relativeMaxMinorAxis=0.5, accuracy=10, highGamma=3):
        self.image = image
        self.scaleFactor = scaleFactor
        self.gamma = gamma
        self.relativeMinMajorAxis = relativeMinMajorAxis
        self.relativeMaxMinorAxis = relativeMaxMinorAxis
        self.accuracy = accuracy

        self.grayImage = rgb2gray(image)
        self.smallGrayImage = self.getGrayRescaledImage()

        self.gamma = gamma
        self.highGamma = highGamma
        if gamma is True:
            # Automatically check if gamma correction is needed
            self.gamma = self.detectGammaNecessity()
            self.smallGrayImage = self.adjustGamma()
        elif gamma is False:
            # Don't apply gamma correction
            pass
        else:
            # Apply gamma correction with the input gamma value
            self.smallGrayImage = self.adjustGamma()

        self.threshold = self.getThreshold()
        self.smallBinaryImage = self.binarizeImage()
        self.contours = self.applyCannyFilter()
        onhRelativeScale = self.defineONHRelativeScale()
        self.minMajorAxis = onhRelativeScale[0]
        self.maxMinorAxis = onhRelativeScale[1]
        self.houghResult = self.applyHoughTransform()
        self.bestSmallScaleEllipse = self.getBestEllipse()

        if self.bestSmallScaleEllipse is None:
            self.bestEllipse = None
        else:
            self.bestEllipse = self.unpackAndUpscaleParameters()


    def getParamsCorrections(self):
        pass
        # Get the scale factor
        # Test for gamma necessity:
        # Look for the image threshold
        # Find the required gamma (min=1, max=?)

    def preProcessImage(self):
        pass
        # Resize image
        # Apply the gamma correction when needed
        # Get the (new) threshold
        # Binarize image
        # Apply the canny filter

    def findOpticNerveHead(self):
        pass
        # apply the elliptical hough transform
        # get the best ellipse approximation
        # rescale



    def getGrayRescaledImage(self):
        outputSize = grayImage.shape[0]//self.scaleFactor, grayImage.shape[1]//self.scaleFactor
        return resize(self.grayImage, outputSize)

    def detectGammaNecessity(self):
        tempThresh = threshold_otsu(self.smallGrayImage)
        if tempThresh > 0.5:
            gamma = self.highGamma
        else:
            gamma = 1
        return gamma

    def adjustGamma(self):
        # only execute if gamma is not False
        return adjust_gamma(self.smallGrayImage, gamma=self.gamma)

    def getThreshold(self):
        # between 0 and 1
        return threshold_otsu(self.smallGrayImage)

    def binarizeImage(self):
        return self.smallGrayImage > self.threshold

    def applyCannyFilter(self):
        return canny(self.smallBinaryImage)

    def defineONHRelativeScale(self):
        xSize = self.smallGrayImage.shape[0]
        ySize = self.smallGrayImage.shape[1]
        minMajorAxis = int(relativeMinMajorAxis*ySize)
        maxMinorAxis = int(relativeMaxMinorAxis*xSize)
        return minMajorAxis, maxMinorAxis

    def applyHoughTransform(self):
        houghResult = hough_ellipse(self.contours,
                                    min_size=self.minMajorAxis,
                                    max_size=self.maxMinorAxis,
                                    accuracy=self.accuracy,
                                    threshold=self.threshold)
        return houghResult

    def getBestEllipse(self):
        self.houghResult.sort(order='accumulator')
        try:
            best = list(self.houghResult[-1])
            return best
        except IndexError:
            # No ellipse corresponding to the input parameters was found
            return None

    def unpackAndUpscaleParameters(self):
        yc, xc, a, b = [int(round(x)*self.scaleFactor) for x in self.bestSmallScaleEllipse[1:5]]
        orientation = best[5]
        yCenter = yc
        xCenter = xc
        minorAxis = a
        majorAxis = b
        orientation = orientation
        return xCenter, yCenter, minorAxis, majorAxis, orientation





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


    # def findClosestEllipse():
    #     """If the ONH was found, approximate it as an ellipse.
    #     Probably returns the circle's center coordinates and radius."""


    # def determineShift():
    #     """Use the position of the ONH circle approximation and find how
    #     far it is from the center of the image, which will give us the shift
    #     value to apply"""
