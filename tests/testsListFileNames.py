import envtest
from processImages import *

class TestListFileNames(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testFindFiles(self):
        directory = "."
        files = listFileNames(directory, "py")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) > 5)

    def testFoundFilesReturnsAListOfStrings(self):
        directory = "."
        files = listFileNames(directory, "py")
        for file in files:
            self.assertTrue(type(file) == str)

    def testSubfoldersNotSearched(self):
        directory = "."
        files = listFileNames(directory, "jpg")
        self.assertTrue(files == [])

    def testDifferentFoldersCanBeReadUsingTheRightPath(self):
        files = listFileNames(self.testSmallFilesDirectory, "jpg")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 1)

if __name__ == "__main__":
    envtest.main()
