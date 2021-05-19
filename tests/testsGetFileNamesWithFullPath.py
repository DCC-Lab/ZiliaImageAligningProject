import envtest
import os
from processImages import *

testFilesDirectory = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"

class TestGetFileNamesWithFullPath(envtest.ZiliaTestCase):
    
    def testInit(self):
        self.assertTrue(True)

    def testFunctionGivesAList(self):
        fileNames = getFilesToInclude(testFilesDirectory, extension="jpg")
        self.assertIsNotNone(fileNames)
        fileNamesWithPath = getFileNamesWithFullPath(testFilesDirectory, fileNames)
        self.assertIsNotNone(fileNamesWithPath)
        self.assertTrue(type(fileNamesWithPath) == list)

    def testFunctionGivesWholePaths(self):
        fileNames = getFilesToInclude(testFilesDirectory, extension="jpg")
        self.assertIsNotNone(fileNames)
        fileNamesWithPath = getFileNamesWithFullPath(testFilesDirectory, fileNames)
        self.assertIsNotNone(fileNamesWithPath)
        for name in fileNamesWithPath:
            self.assertTrue(os.path.exists(name))


if __name__ == "__main__":
    envtest.main()
