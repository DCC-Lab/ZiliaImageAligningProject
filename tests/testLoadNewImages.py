import envtest
from processImages import *
import numpy as np

oldFilesTestDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample"
newFilesTestDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"


class TestLoadNewImages(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportNewFiles(self):
        newImages = loadNewImages(newFilesTestDir)
        self.assertIsNotNone(newImages)
        self.assertTrue(len(newImages) > 0)
        self.assertTrue(len(newImages) < 100)

    def testImportOldFiles(self):
        oldImages = loadNewImages(oldFilesTestDir)
        self.assertIsNotNone(oldImages)
        self.assertTrue(len(oldImages) > 0)
        self.assertTrue(len(oldImages) < 100)

    def testImportOldFilesDoesTheSameAsTheOldFunction(self):
        imagesOldFunction = loadImages(oldFilesTestDir)
        self.assertIsNotNone(imagesOldFunction)
        imagesNewFunction = loadNewImages(oldFilesTestDir)
        self.assertIsNotNone(imagesNewFunction)
        equalityTest = np.equal(imagesOldFunction, imagesNewFunction)
        self.assertTrue(equalityTest.all())


if __name__ == "__main__":
    envtest.main()
