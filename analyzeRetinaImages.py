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
from skimage.transform import resize, hough_ellipse
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.exposure import adjust_gamma


class EllipseDetector:
    """
    This is the order in which this should be used:
        detector = EllipseDetector(image)
        detector.preProcessImage()
        bestEllipse = detector.findBestEllipse
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
    """

    def __init__(self, image, relativeMinMajorAxis=1/6, relativeMaxMinorAxis=0.5, accuracy=10):
        self.image = image
        self.relativeMinMajorAxis = relativeMinMajorAxis
        self.relativeMaxMinorAxis = relativeMaxMinorAxis
        self.accuracy = accuracy
        if len(image.shape) == 2:
            self.grayImage = image
        else:
            self.grayImage = rgb2gray(image)

    def preProcessImage(self):
        self.contours = self.applyCannyFilter()
        ellipseExpectedSize = self.defineEllipseExpectedSize()
        self.minMajorAxis = ellipseExpectedSize[0]
        self.maxMinorAxis = ellipseExpectedSize[1]

    def findBestEllipse(self):
        """
        If no ellipse is found, returns None.
        Else, returns a tuple of the best ellipse parameters.
        """
        houghResult = self.applyHoughTransform()
        bestHoughEllipse = self.sortBestHoughEllipse(houghResult)
        bestEllipse = self.getBestEllipseParameters(bestHoughEllipse)
        return bestEllipse

    def applyCannyFilter(self):
        print("If this prints, THIS IS WRONG!!!")
        return canny(self.grayImage)

    def defineEllipseExpectedSize(self):
        xSize = self.grayImage.shape[0]
        ySize = self.grayImage.shape[1]
        minMajorAxis = int(self.relativeMinMajorAxis*ySize)
        maxMinorAxis = int(self.relativeMaxMinorAxis*xSize)
        return minMajorAxis, maxMinorAxis

    def applyHoughTransform(self):
        houghResult = hough_ellipse(self.contours,
                                    min_size=self.minMajorAxis,
                                    max_size=self.maxMinorAxis,
                                    accuracy=self.accuracy)
        return houghResult

    def sortBestHoughEllipse(self, houghResult):
        houghResult.sort(order='accumulator')
        try:
            best = list(houghResult[-1])
            return best
        except IndexError:
            # No ellipse corresponding to the input parameters was found
            return None

    def getBestEllipseParameters(self, bestHoughEllipse):
        if bestHoughEllipse is None:
            return None
        yc, xc, a, b = [int(round(x)) for x in bestHoughEllipse[1:5]]
        orientation = bestHoughEllipse[5]
        yCenter = yc
        xCenter = xc
        minorAxis = a
        majorAxis = b
        orientation = orientation
        return (xCenter, yCenter), minorAxis, majorAxis, orientation


class ZiliaONHDetector(EllipseDetector):
    """
    This is the order in which this should be used:
        onhDetector = ZiliaONHDetector(image)
        detector.getParamsCorrections()
        detector.preProcessImage()
        bestEllipse = detector.findBestEllipse
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
    """

    def __init__(self, image, scaleFactor=3, gamma=True, relativeMinMajorAxis=1/6, relativeMaxMinorAxis=0.5, accuracy=10):
        self.fullSizeGrayImage = rgb2gray(image)
        super(ZiliaONHDetector, self).__init__(image, relativeMinMajorAxis, relativeMaxMinorAxis, accuracy)
        self.scaleFactor = scaleFactor
        self.gamma = gamma
        self.grayImage = self.getGrayRescaledImage()

    def getParamsCorrections(self, highGamma=3):
        """Find the required gamma correction (min=1, max=?)"""
        self.highGamma = highGamma
        if self.gamma is True:
            # Automatically check if gamma correction is needed
            self.gamma = self.detectGammaNecessity()
        elif self.gamma is False:
            # Don't apply gamma correction
            pass
        elif int(self.gamma) == 1:
            # No need to apply gamma correction
            self.gamma = False
        else:
            # Apply gamma correction with the input gamma value
            self.smallGrayImage = self.adjustGamma()

    def preProcessImage(self):
        self.smallGrayImage = self.adjustGamma()
        self.threshold = self.getThreshold()
        super(ZiliaONHDetector, self).preProcessImage()

    def detectGammaNecessity(self):
        # Has to be improved with testing!!!
        tempThresh = self.getThreshold()
        if tempThresh > 0.5:
            gamma = self.highGamma
        else:
            gamma = 1
        return gamma

    def adjustGamma(self):
        if self.gamma is False:
            return self.smallGrayImage
        else:
            return adjust_gamma(self.smallGrayImage, gamma=self.gamma)

    def findOpticNerveHead(self):
        smallScaleResult = super(ZiliaONHDetector, self).findBestEllipse()
        for coord in smallScaleResult:
            if coord is None:
                return smallScaleResult
        
        if self.bestSmallScaleEllipse is None:
            self.bestEllipse = None
        else:
            self.bestEllipse = self.unpackAndUpscaleParameters()
        return self.bestEllipse

    def getGrayRescaledImage(self):
        outputSize = fullSizeGrayImage.shape[0]//self.scaleFactor, fullSizeGrayImage.shape[1]//self.scaleFactor
        return resize(self.fullSizeGrayImage, outputSize)

    def getThreshold(self):
        # Between 0 and 1
        return threshold_otsu(self.grayImage)

    def applyCannyFilter(self):
        print("If this prints, THIS IS RIGHT!!!")
        binaryImage = self.grayImage > self.threshold
        return canny(binaryImage)

    def unpackAndUpscaleParameters(self):
        yc, xc, a, b = [int(round(x)*self.scaleFactor) for x in self.bestSmallScaleEllipse[1:5]]
        orientation = best[5]
        yCenter = yc
        xCenter = xc
        minorAxis = a
        majorAxis = b
        orientation = orientation
        return (xCenter, yCenter), minorAxis, majorAxis, orientation
