import numpy as np
from ellipse import LsqEllipse
from skimage.color import rgb2gray
from skimage.transform import resize, hough_ellipse
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.exposure import adjust_gamma


class EllipseDetector:
    """
    The relative size of the ellipse is defined as a fraction of the largest
    side of the input image.
    Ellipse orientation in radians, counterclockwise.

    This is the order in which this should be used:
        detector = EllipseDetector(image)
        detector.preProcessImage()
        bestEllipse = detector.findBestEllipse()
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
    """

    def __init__(self, image, relativeMinMajorAxis=1/5, relativeMaxMinorAxis=0.5,
                    relativeMaxMajorAxis=3/4, relativeMinMinorAxis=1/8, accuracy=10):
        self.image = image
        self.relativeMinMajorAxis = relativeMinMajorAxis
        self.relativeMaxMinorAxis = relativeMaxMinorAxis
        self.relativeMaxMajorAxis = relativeMaxMajorAxis
        self.relativeMinMinorAxis = relativeMinMinorAxis
        self.accuracy = accuracy
        if self.imageIsGrayscale():
            self.grayImage = image
        else:
            self.grayImage = rgb2gray(image)

    def imageIsGrayscale(self):
        return len(self.image.shape) == 2

    def preProcessImage(self):
        self.contours = self.applyCannyFilter()
        ellipseExpectedSize = self.defineEllipseExpectedSize()
        self.minMajorAxis = ellipseExpectedSize[0]
        self.maxMinorAxis = ellipseExpectedSize[1]
        self.maxMajorAxis = ellipseExpectedSize[2]
        self.minMinorAxis = ellipseExpectedSize[3]


    def findBestEllipse(self):
        """
        If no ellipse is found, returns None.
        Else, returns a tuple of the best ellipse parameters.
        """
        leastSquaresResult = self.doLeastSquaresEllipseFit()
        if leastSquaresResult is not None:
            (yCenter, xCenter), normalHalfAx, parallelHalfAx, orientation = leastSquaresResult
            bestEllipse = (xCenter, yCenter), normalHalfAx, parallelHalfAx, orientation
            return bestEllipse
        else:
            # The least squares algorithm has failed.
            houghResult = self.applyHoughTransform()
            bestHoughEllipse = self.sortBestHoughEllipse(houghResult)
            bestEllipse = self.getBestEllipseParameters(bestHoughEllipse)
            if bestEllipse is None:
                return None
            (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
            minAxis = min([minorAxis, majorAxis])
            maxAxis = max([minorAxis, majorAxis])
            if self.ellipseHasTheRightSize(minAxis, maxAxis):
                return bestEllipse
            return None

    def applyCannyFilter(self):
        return canny(self.grayImage)

    def defineEllipseExpectedSize(self):
        xSize = self.grayImage.shape[1]
        ySize = self.grayImage.shape[0]
        maxSide = max([xSize, ySize])
        minMajorAxis = int(self.relativeMinMajorAxis*maxSide)
        maxMinorAxis = int(self.relativeMaxMinorAxis*maxSide)
        maxMajorAxis = int(self.relativeMaxMajorAxis*maxSide)
        minMinorAxis = int(self.relativeMinMinorAxis*maxSide)
        return minMajorAxis, maxMinorAxis, maxMajorAxis, minMinorAxis

    def ellipseHasTheRightSize(self, minAxis, maxAxis):
        minAxis *= 2
        maxAxis *= 2
        if minAxis > self.minMinorAxis:
            if minAxis < self.maxMinorAxis:
                if maxAxis > self.minMajorAxis:
                    if maxAxis < self.maxMajorAxis:
                        return True
        return False


    def doLeastSquaresEllipseFit(self):
        X, Y = np.where(self.contours == True)
        contoursIndexes = np.array(list(zip(X, Y)))

        lsqFit = LsqEllipse().fit(contoursIndexes)
        center, normalHalfAx, parallelHalfAx, phi = lsqFit.as_parameters()


        minAxis = min([normalHalfAx, parallelHalfAx])
        maxAxis = max([normalHalfAx, parallelHalfAx])
        if self.ellipseHasTheRightSize(minAxis, maxAxis):
            return bestEllipse
        else:
            pass


    def addGammaCorrection(self, gamma):
        correctedImage = adjust_gamma(self.grayImage, gamma=gamma)
        return correctedImage


    def filterLeastSquaresEllipseFit(self):
        # check size (if horiz >> vertic: not good, but horiz = vertic or a bit bigger is ok)
        # check angle to know which is bigger?
        # If size not ok, gamma correction
        # If size still not ok, gamma correction
        # Do the same a few times.
        # If size ok, remove out of range indexes
        # If size not ok after a few gamma corrections, return None
        pass


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
        orientation = np.pi - orientation
        return (xCenter, yCenter), minorAxis, majorAxis, orientation


class ZiliaONHDetector(EllipseDetector):
    """
    The relative size of the ellipse is defined as a fraction of the largest
    side of the input image.
    Ellipse orientation in radians, counterclockwise.

    This is the order in which this should be used:
        onhDetector = ZiliaONHDetector(image)
        onhDetector.getParamsCorrections()
        onhDetector.preProcessImage()
        bestEllipse = onhDetector.findOpticNerveHead()
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
    """

    def __init__(self, image, scaleFactor=5, gamma=True, relativeMinMajorAxis=1/5,
                    relativeMaxMinorAxis=0.5, relativeMaxMajorAxis=3/4, relativeMinMinorAxis=1/8, accuracy=10):
        super(ZiliaONHDetector, self).__init__(image, relativeMinMajorAxis, relativeMaxMinorAxis, accuracy)
        self.fullSizeGrayImage = np.array(self.grayImage, copy=True)
        self.scaleFactor = scaleFactor
        self.gamma = gamma
        self.grayImage = self.getGrayRescaledImage()

    def getParamsCorrections(self, highGamma=3, gammaThresh=0.5):
        """Find the required gamma correction (min=1, max=?)"""
        self.highGamma = highGamma
        if self.gamma is True:
            # Automatically check if gamma correction is needed
            self.gamma = self.detectGammaNecessity(gammaThresh=gammaThresh)
        elif self.gamma is False:
            # Don't apply gamma correction whatsoever
            pass
        elif int(self.gamma) == 1:
            # No need to apply gamma correction
            self.gamma = False
        else:
            # Apply gamma correction with the input gamma value
            self.grayImage = self.adjustGamma()

    def preProcessImage(self):
        self.grayImage = self.adjustGamma()
        self.threshold = self.getThreshold()
        super(ZiliaONHDetector, self).preProcessImage()

    def findOpticNerveHead(self):
        smallScaleResult = super(ZiliaONHDetector, self).findBestEllipse()
        if smallScaleResult is None:
            return smallScaleResult
        else:
            result = self.upscaleResult(smallScaleResult)
            return result

    def detectGammaNecessity(self, gammaThresh=0.5):
        # Has to be improved with testing!!!
        tempThresh = self.getThreshold()
        if tempThresh > gammaThresh:
            gamma = self.highGamma
            print("gamma done!")
        else:
            gamma = 1
        return gamma

    def adjustGamma(self):
        if self.gamma is False:
            return self.grayImage
        else:
            return adjust_gamma(self.grayImage, gamma=self.gamma)

    def getGrayRescaledImage(self):
        ySize = self.fullSizeGrayImage.shape[0]//self.scaleFactor
        xSize = self.fullSizeGrayImage.shape[1]//self.scaleFactor
        outputSize = ySize, xSize
        return resize(self.fullSizeGrayImage, outputSize)

    def getThreshold(self):
        # Between 0 and 1
        return threshold_otsu(self.grayImage)

    def applyCannyFilter(self):
        binaryImage = self.grayImage > self.threshold
        return canny(binaryImage)

    def upscaleResult(self, smallScaleResult):
        (xCenter, yCenter), minAxis, majAxis, orientation = smallScaleResult
        xCenter = self.scaleFactor*xCenter
        yCenter = self.scaleFactor*yCenter
        minAxis = self.scaleFactor*minAxis
        majAxis = self.scaleFactor*majAxis
        return (xCenter, yCenter), minAxis, majAxis, orientation


"""
###############################
Notes for new, faster algorithm
###############################

I will need to check the following:
- Large axis size
- Small axis size
- Orientation (to see where are the biggest/smallest axis to see how to
    determine which is the width and which is the height)

I will thus have to put maximum and minimum sizes for both large and small
axis.
I will also need to apply the following corrections:
- Delete out of range indexes for the found ellipses
- If an ellipse of reasonable size has not been found, apply some gamma
    correction. If still not good, apply more gamma correction. Do this maybe
    starting with gamma==1.5 and raise the number 0.5 at each iteration, then
    stop when a good size ellipse is found or when gamma==10, maybe. If still
    no good match, try with the elliptical Hough transform. From there, just
    go with the old algorithm.
"""
