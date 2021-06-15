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

    def __init__(self, image, grayImage=False, relativeMinMajorAxis=1/6, relativeMaxMinorAxis=0.5, accuracy=10):
        self.image = image
        self.relativeMinMajorAxis = relativeMinMajorAxis
        self.relativeMaxMinorAxis = relativeMaxMinorAxis
        self.accuracy = accuracy
        if grayImage:
            self.grayImage = image
        else:
            self.grayImage = rgb2gray(image)

    def binarizeImage(self):
        return self.grayImage > self.threshold

    def applyCannyFilter(self):
        return canny(self.binaryImage)

    def defineEllipseExpectedSize(self):
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

    def unpackParameters(self):
        yc, xc, a, b = [int(round(x)) for x in self.bestSmallScaleEllipse[1:5]]
        orientation = best[5]
        yCenter = yc
        xCenter = xc
        minorAxis = a
        majorAxis = b
        orientation = orientation
        return (xCenter, yCenter), minorAxis, majorAxis, orientation


class ZiliaONHDetector(EllipseDetector):

    def __init__(self, image, scaleFactor=3, gamma=True, relativeMinMajorAxis=1/6, relativeMaxMinorAxis=0.5, accuracy=10):
        self.image = image
        self.scaleFactor = scaleFactor
        self.gamma = gamma
        self.relativeMinMajorAxis = relativeMinMajorAxis
        self.relativeMaxMinorAxis = relativeMaxMinorAxis
        self.accuracy = accuracy
        self.grayImage = rgb2gray(image)
        self.smallGrayImage = self.getGrayRescaledImage()

    def getParamsCorrections(self, highGamma=3):
        """Find the required gamma correction (min=1, max=?)"""
        self.highGamma = highGamma
        if self.gamma is True:
            # Automatically check if gamma correction is needed
            self.gamma = self.detectGammaNecessity()
        elif gamma is False:
            # Don't apply gamma correction
            pass
        else:
            # Apply gamma correction with the input gamma value
            self.smallGrayImage = self.adjustGamma()

    def preProcessImage(self):
        if self.gamma == 1:
            # No need to apply gamma correction
            pass
        else:
            self.smallGrayImage = self.adjustGamma()
        self.threshold = self.getThreshold()
        self.smallBinaryImage = self.binarizeImage()
        contours = self.applyCannyFilter()
        self.preProcessedImage = self.contours

    def findOpticNerveHead(self):
        expectedONHSize = self.defineONHExpectedSize()
        self.minMajorAxis = expectedONHSize[0]
        self.maxMinorAxis = expectedONHSize[1]
        self.houghResult = self.applyHoughTransform()
        self.bestSmallScaleEllipse = self.getBestEllipse()
        if self.bestSmallScaleEllipse is None:
            self.bestEllipse = None
        else:
            self.bestEllipse = self.unpackAndUpscaleParameters()
        return self.bestEllipse

    def getGrayRescaledImage(self):
        outputSize = grayImage.shape[0]//self.scaleFactor, grayImage.shape[1]//self.scaleFactor
        return resize(self.grayImage, outputSize)

    def detectGammaNecessity(self):
        # Has to be improved with testing!!!
        tempThresh = self.getThreshold()
        if tempThresh > 0.5:
            gamma = self.highGamma
        else:
            gamma = 1
        return gamma

    def adjustGamma(self):
        # Only execute if gamma is not False
        return adjust_gamma(self.smallGrayImage, gamma=self.gamma)

    def getThreshold(self):
        # Between 0 and 1
        return threshold_otsu(self.smallGrayImage)

    def binarizeImage(self):
        return self.smallGrayImage > self.threshold

    def applyCannyFilter(self):
        return canny(self.smallBinaryImage)

    def defineONHExpectedSize(self):
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
        return (xCenter, yCenter), minorAxis, majorAxis, orientation

