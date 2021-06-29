import envtest
import os
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from processImages import listFileNames, getFiles
from analyzeRetinaImages import ZiliaONHDetector
from skimage.draw import ellipse, ellipse_perimeter
import math
import json

"""
WARNING: These tests will fail on another computer if the test files path
is not changed!
"""

# The inputs are original retina images with visible ONH
# The outputs are the binary images that have been manually fitted
inputsPath = r"E:\AAA_Reference images\ManuallySorted/inputs"
outputsPath = r"E:\AAA_Reference images\ManuallySorted/outputs"

# These values will be to find which one gives the best success rate when they
# are used as thresholds to apply gamma correction
mean = 0.5301227941321696
meanMinHalfSigma = 0.4891183892357014
meanMinSigma = 0.4481139843392332
meanMin2Sigma = 0.36610517454629693

# @envtest.skip("Will fail if path is not changed")
class testsEllipseDetectionSuccess(envtest.ZiliaTestCase):

    def testAccessData(self):
        listDirIn = os.listdir(inputsPath)
        listDirOut = os.listdir(outputsPath)
        self.assertTrue(len(listDirIn) > 1)
        self.assertTrue(len(listDirOut) > 1)
        # print(listDirOut)
        # print(listDirIn)

    def testSortFileNames(self):
        sortedFileNames = np.sort(listFileNames(inputsPath))
        self.assertTrue(len(sortedFileNames) > 1)
        # print(sortedFileNames)

    def testFileNamesAreTheSameForInsAndOuts(self):
        sortedInputs = np.sort(listFileNames(inputsPath))
        sortedOutputs = np.sort(listFileNames(outputsPath))
        self.assertTrue(len(sortedInputs) == len(sortedOutputs))
        for i in range(len(sortedInputs)):
            self.assertTrue(sortedInputs[i] == sortedOutputs[i])

    @envtest.skip("skip plots")
    def testOutputImageIntoBinary(self):
        sortedOutputs = getFiles(outputsPath, newImages=False)
        testImage = imread(sortedOutputs[0], as_gray=True)
        self.assertTrue(len(testImage.shape) == 2)
        lower = 0
        upper = 1
        threshold = 0.5
        binaryImage = np.where(testImage >= threshold, upper, lower)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(testImage)
        plt.subplot(1,2,2)
        plt.imshow(binaryImage)
        plt.show()

    def binarizeImage(self, colorImagePath):
        grayImage = imread(colorImagePath, as_gray=True)
        lower = 0
        upper = 1
        threshold = 0.5
        binaryImage = np.where(grayImage >= threshold, upper, lower)
        return binaryImage

    @envtest.skip("skip plots")
    def testBinarizeImage(self):
        sortedInputs = getFiles(inputsPath, newImages=False)
        sortedOutputs = getFiles(outputsPath, newImages=False)
        testInput = imread(sortedInputs[0])
        testOutput = self.binarizeImage(sortedOutputs[0])
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(testInput)
        plt.subplot(1,2,2)
        plt.imshow(testOutput, cmap="gray")
        plt.show()

    @envtest.skip("skip plots")
    def testDrawFullEllipse(self):
        testImage = imread(self.testStudentDirectory+"/testImage1.png")
        onhDetector = ZiliaONHDetector(testImage)
        onhDetector.getParamsCorrections()
        onhDetector.preProcessImage()
        bestEllipse = onhDetector.findOpticNerveHead()
        if bestEllipse is None:
            self.assertFalse(True)
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse

        yPoints, xPoints = ellipse(yCenter, xCenter, minorAxis, majorAxis, rotation=orientation)

        imageWithEllipse = np.zeros((testImage.shape[0], testImage.shape[1]))
        imageWithEllipse[yPoints, xPoints] = 1
        # print(imageWithEllipse)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(testImage)
        plt.subplot(1,2,2)
        plt.imshow(imageWithEllipse, cmap="gray")
        plt.show()

    def getBestEllipse(self, image, highGamma=3, gammaThresh=0.5):
        onhDetector = ZiliaONHDetector(image)
        onhDetector.getParamsCorrections(highGamma=highGamma, gammaThresh=gammaThresh)
        onhDetector.preProcessImage()
        bestEllipse = onhDetector.findOpticNerveHead()
        return bestEllipse

    def getImageWithFullEllipse(self, bestEllipse, originalImage):
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
        if orientation > math.pi:
            orientation -= 2*math.pi
        yPoints, xPoints = ellipse(yCenter, xCenter, minorAxis, majorAxis, rotation=-orientation)
        imageWithEllipse = np.zeros((originalImage.shape[0], originalImage.shape[1]))
        imageWithEllipse[yPoints, xPoints] = 1
        return imageWithEllipse

    def getImageWithEmptyEllipse(self, bestEllipse, originalImage):
        (xCenter, yCenter), minorAxis, majorAxis, orientation = bestEllipse
        if orientation > math.pi:
            orientation -= 2*math.pi
        yPoints, xPoints = ellipse_perimeter(yCenter, xCenter, minorAxis, majorAxis, orientation=orientation)
        imageWithEllipse = np.zeros((originalImage.shape[0], originalImage.shape[1]))
        imageWithEllipse[yPoints, xPoints] = 1
        return imageWithEllipse

    def plotOriginalImageNextToFit(self, originalImage, imageWithEllipse):
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(originalImage)
        plt.subplot(1,2,2)
        plt.imshow(imageWithEllipse, cmap="gray")
        plt.show()

    @envtest.skip("skip plots")
    def testEllipseFunctions(self):
        testInput = imread(self.testStudentDirectory+"/testImage1.png")
        bestEllipse = self.getBestEllipse(testInput)
        if bestEllipse is None:
            self.assertFalse(True)
        imageWithEllipse = self.getImageWithFullEllipse(bestEllipse, testInput)
        self.plotOriginalImageNextToFit(testInput, imageWithEllipse)

    @envtest.skip("skip plots")
    def testCompareEllipseAndEllipsePerimeter(self):
        testInput = imread(self.testStudentDirectory+"/testImage4.png")
        bestEllipse = self.getBestEllipse(testInput)
        if bestEllipse is None:
            self.assertFalse(True)
        imageWithEllipse = self.getImageWithFullEllipse(bestEllipse, testInput)
        imageWithEllipsePerimeter = self.getImageWithEmptyEllipse(bestEllipse, testInput)
        self.plotOriginalImageNextToFit(imageWithEllipsePerimeter, imageWithEllipse)
        # So "orientation" in ellipse_perimeter seems to be the same as
        # "-rotation" in ellipse.

    @envtest.skip("skip plots")
    def testEllipseFunctionsOnRealImage(self):
        sortedInputs = getFiles(inputsPath, newImages=False)
        testInput = imread(sortedInputs[0])
        bestEllipse = self.getBestEllipse(testInput)
        if bestEllipse is None:
            self.assertFalse(True)
        imageWithEllipse = self.getImageWithFullEllipse(bestEllipse, testInput)
        imageWithEllipsePerimeter = self.getImageWithEmptyEllipse(bestEllipse, testInput)
        self.plotOriginalImageNextToFit(testInput, imageWithEllipse)
        self.plotOriginalImageNextToFit(testInput, imageWithEllipsePerimeter)

    @envtest.skip("skip computing time")
    def testFindSuccessRateOn1File(self):
        sortedInputs = getFiles(inputsPath, newImages=False)
        sortedOutputs = getFiles(outputsPath, newImages=False)
        testInput = imread(sortedInputs[0])
        testOutput = self.binarizeImage(sortedOutputs[0])
        bestEllipse = self.getBestEllipse(testInput)
        if bestEllipse is None:
            self.assertFalse(True)
        imageWithEllipse = self.getImageWithFullEllipse(bestEllipse, testInput)
        resultMatrix = imageWithEllipse + testOutput
        self.assertTrue(np.max(resultMatrix) == 2)
        self.assertTrue(np.min(resultMatrix) == 0)

        values, counts = np.unique(resultMatrix, return_counts=True)
        results = dict(zip(values, counts))
        self.assertTrue(len(results) == 3)

        imageShape = testInput.shape
        numberOfValues = imageShape[0]*imageShape[1]

        result = ((numberOfValues - results[1])/numberOfValues)*100
        print("success % = ", result, "%") # 93.82956511054942 %

    @envtest.skip("skip computing time")
    def testFindSuccessRateOn4FileWithGammaThreshEqualsMean(self):
        sortedInputs = getFiles(inputsPath, newImages=False)[:4]
        sortedOutputs = getFiles(outputsPath, newImages=False)[:4]
        sortedFileNames = np.sort(listFileNames(inputsPath))
        resultsList = []
        resultsDict = {}
        for i in range(len(sortedInputs)):
            print(f"image index {i} being analyzed")
            testInput = imread(sortedInputs[i])
            testOutput = self.binarizeImage(sortedOutputs[i])
            bestEllipse = self.getBestEllipse(testInput, highGamma=3, gammaThresh=globalMean)
            if bestEllipse is None:
                self.assertFalse(True)
            imageWithEllipse = self.getImageWithFullEllipse(bestEllipse, testInput)
            resultMatrix = imageWithEllipse + testOutput
            self.plotOriginalImageNextToFit(testInput, imageWithEllipse)

            values, counts = np.unique(resultMatrix, return_counts=True)
            results = dict(zip(values, counts))

            imageShape = testInput.shape
            numberOfValues = imageShape[0]*imageShape[1]

            result = (numberOfValues - results[1])/numberOfValues
            resultsList.append(result)

        mean = np.mean(resultsList)
        std = np.std(resultsList)

        print("resultsList = ", resultsList) # [0.9382956511054943, 0.966275084252451, 0.9911971746706495, 0.9869382771012051]
        print("mean = ", mean) # 0.97067654678245
        print("std = ", std) # 0.020937020556485244

    def testSaveDictToJsonFile(self):
        testDictionary = {0:51, 1:49, 2:72}
        with open('dictionarySaveTest.json', 'w') as file:
            json.dump(testDictionary, file,  indent=4)

    


globalMean = 0.5301227941321696
meanMinHalfSigma = 0.4891183892357014
meanMinSigma = 0.4481139843392332
meanMin2Sigma = 0.36610517454629693

if __name__ == "__main__":
    envtest.main()
