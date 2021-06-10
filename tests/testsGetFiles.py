import envtest
from processImages import *
import os

class TestGetFiles(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testGetFilesReturnsTheRigtOutput(self):
        directory = self.testFilesDirectory
        files = getFiles(directory)
        self.assertIsNotNone(files)
        self.assertTrue(type(files) == list)

    def testOldReturnsAllFiles(self):
        directory = self.testFilesDirectory
        files = getFiles(directory, newImages=False)
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == len(os.listdir(directory)))

    def testNewDoesNotReturnAllFiles(self):
        # newImages is set to True by default, so no need to specify it.
        directory = self.testFilesDirectory
        files = getFiles(directory)
        self.assertTrue(len(files) < len(os.listdir(directory)))

    def testGetFilesDoesNotReturnTheWrongFiles(self):
        directory = self.testFilesDirectory
        files = getFiles(directory)
        # print(files)
        for file in files:
            if "eye" in file.lower():
                if "rosa" in file.lower():
                    self.assertTrue(False)
        self.assertTrue(True)

if __name__ == "__main__":
    envtest.main()
