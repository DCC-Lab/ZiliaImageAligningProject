import envtest
import os
import numpy as np
from processImages import listFileNames, getFiles
from skimage.io import imread

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

    def testOutputImageIntoBinary(self):
        sortedOutputs = getFiles(inputsPath, newImages=False)
        testImage = imread(sortedOutputs[0], as_gray=True)
        self.assertTrue(len(testImage.shape) == 2)

if __name__ == "__main__":
    envtest.main()
