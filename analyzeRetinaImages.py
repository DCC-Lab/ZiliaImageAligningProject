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
        self.contours = self.applyCannyFilter(self.grayImage)
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
        leastSquaresResult = self.getLeastSquaresEllipseFit(self.contours)
        if leastSquaresResult is not None:
            bestEllipse = leastSquaresResult
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

    def applyCannyFilter(self, grayImage):
        return canny(grayImage)

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

    def doLeastSquaresEllipseFit(self, contours):
        X, Y = np.where(contours == True)
        contoursIndexes = np.array(list(zip(X, Y)))
        lsqFit = LsqEllipse().fit(contoursIndexes)
        lsqResult = lsqFit.as_parameters()
        return lsqResult

    def getLeastSquaresEllipseFit(self, contours):
        gammas = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 15, 20, 1]
        for gamma in gammas:
            # Try with 16 different gamma values
            lsqResult = self.doLeastSquaresEllipseFit(contours)
            (yCenter, xCenter), normalHalfAx, parallelHalfAx, orientation = lsqResult
            minAxis = min([normalHalfAx, parallelHalfAx])
            maxAxis = max([normalHalfAx, parallelHalfAx])
            if self.ellipseHasTheRightSize(minAxis, maxAxis):
                # Order the parameters before returning them
                if parallelHalfAx > normalHalfAx:
                    majorAxis = parallelHalfAx
                    minorAxis = normalHalfAx
                else:
                    orientation += (np.pi/2)
                    majorAxis = normalHalfAx
                    minorAxis = parallelHalfAx
                bestEllipse = (xCenter, yCenter), minorAxis, majorAxis, orientation
                return bestEllipse
            else:
                if gamma == 1:
                    # stop at last iteration
                    break
                # Apply gamma correction and try again
                correctedImage = self.doGammaCorrection(gamma)
                contours = self.applyCannyFilter(correctedImage)
        # If the code goes here, no ellipse of the expected size was found
        return None

    def doGammaCorrection(self, gamma):
        correctedImage = adjust_gamma(self.grayImage, gamma=gamma)
        return correctedImage

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
            return None
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
