import envtest
import os
from processImages import *

class TestGetFilePaths(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testFunctionGivesAList(self):
        fileNames = getFilesToInclude(self.testFilesDirectory, extension="jpg")
        self.assertIsNotNone(fileNames)
        fileNamesWithPath = getFilePaths(self.testFilesDirectory, fileNames)
        self.assertIsNotNone(fileNamesWithPath)
        self.assertTrue(type(fileNamesWithPath) == list)

    def testFunctionGivesWholePaths(self):
        fileNames = getFilesToInclude(self.testFilesDirectory, extension="jpg")
        self.assertIsNotNone(fileNames)
        fileNamesWithPath = getFilePaths(self.testFilesDirectory, fileNames)
        self.assertIsNotNone(fileNamesWithPath)
        for name in fileNamesWithPath:
            self.assertTrue(os.path.exists(name))
        # print(fileNamesWithPath)
        # print(np.sort(fileNamesWithPath))


if __name__ == "__main__":
    envtest.main()
