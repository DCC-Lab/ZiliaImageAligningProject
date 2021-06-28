import envtest
import os
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from processImages import listFileNames, getFiles
from analyzeRetinaImages import ZilaONHDetector

"""
WARNING: These tests will fail on another computer if the test files path
is not changed!
"""

# The outputs are the binary images that have been manually fitted
inputsPath = r"E:\AAA_Reference images\ManuallySorted/inputs"
outputsPath = r"E:\AAA_Reference images\ManuallySorted/outputs"

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

    def testFindSuccessRateOn1File(self):
        sortedInputs = getFiles(inputsPath, newImages=False)
        sortedOutputs = getFiles(outputsPath, newImages=False)
        testInput = imread(sortedInputs[0])
        testOutput = self.binarizeImage(sortedOutputs[0])


if __name__ == "__main__":
    envtest.main()
