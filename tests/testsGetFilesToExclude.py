import sys
import envtest
from processImages import *

testFilesDirectory = r"TestImages/miniTestSampleNewData/"
# sys.path.insert(0, directory)

# I want to make shure ONLY the right files are excluded, NOTHING ELSE.
class TestGetFilesToExclude(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testFilesDirectoryIsAccessible(self):
        listOfFiles = listNameOfFiles(testFilesDirectory, extension="jpg")
        self.assertTrue(len(listOfFiles) > 0)
        self.assertTrue(len(listOfFiles) < 30)

    def testOnlyTheRightFilesAreExcluded(self):
        excludedFiles = getFilesToExclude(testFilesDirectory, extension="jpg")
        for imageName in excludedFiles:
            self.assertTrue("eye" in imageName.lower())
            self.assertTrue("rosa" in imageName.lower())

if __name__ == "__main__":
    envtest.main()
