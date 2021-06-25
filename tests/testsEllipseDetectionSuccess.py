import envtest
import os
"""
WARNING: These tests will fail on another computer if the test files path
is not changed!
"""

inputsPath = r"E:\AAA_Reference images\ManuallySorted/inputs"
outputsPath = r"E:\AAA_Reference images\ManuallySorted/outputs"

class testsEllipseDetectionSuccess(envtest.ZiliaTestCase):

    def testAccessData(self):
        listDirIn = os.listdir(inputsPath)
        listDirOut = os.listdir(outputsPath)
        self.assertTrue(len(listDirIn) > 1)
        self.assertTrue(len(listDirOut) > 1)
        # print(listDirOut)
        # print(listDirIn)

if __name__ == "__main__":
    envtest.main()
