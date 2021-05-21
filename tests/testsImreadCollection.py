import envtest
from skimage.io import imread_collection
from processImages import *
import numpy as np

# testFilesDirectory = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"
testDirectory = "./TestImages"

class TestImreadCollection(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testFunctionGetsImages(self):
        collectionWithDir = imread_collection(testDirectory+"/*.jpg")
        self.assertIsNotNone(collectionWithDir)
        self.assertTrue(len(collectionWithDir) > 0)
        self.assertTrue(len(collectionWithDir) < 10)


    def testDirectoryPathAndListOfPathsReturnMatricesWithSameLength(self):
        collectionWithDir = imread_collection(testDirectory+"/*.jpg")
        self.assertIsNotNone(collectionWithDir)
        listOfFiles = listNameOfFiles(testDirectory, extension="jpg")
        self.assertIsNotNone(listOfFiles)
        listOfPaths = getFilePaths(testDirectory, listOfFiles)
        self.assertIsNotNone(listOfPaths)
        collectionWithPaths = imread_collection(listOfPaths)
        self.assertIsNotNone(collectionWithPaths)
        self.assertTrue(len(collectionWithDir) > 0)
        self.assertTrue(len(collectionWithPaths) > 0)
        self.assertTrue(len(collectionWithDir) == len(collectionWithPaths))
        # print(collectionWithDir)
        # print(collectionWithPaths)
        # self.assertFalse(collectionWithDir is collectionWithPaths)
        # self.assertTrue(collectionWithDir == collectionWithPaths)


    def testDirectoryPathAndListOfPathsDontReturnEqualMatrices(self):
        collectionWithDir = imread_collection(testDirectory+"/*.jpg")
        self.assertIsNotNone(collectionWithDir)
        listOfFiles = listNameOfFiles(testDirectory, extension="jpg")
        self.assertIsNotNone(listOfFiles)
        listOfPaths = getFilePaths(testDirectory, listOfFiles)
        self.assertIsNotNone(listOfPaths)
        collectionWithPaths = imread_collection(listOfPaths)
        self.assertIsNotNone(collectionWithPaths)
        self.assertFalse(collectionWithDir is collectionWithPaths)
        self.assertFalse(collectionWithDir == collectionWithPaths)
        # print(collectionWithDir)
        # print(collectionWithPaths)


    def testDirectoryPathAndListOfPathsReturnEqualSubmatrices(self):
        collectionWithDir = imread_collection(testDirectory+"/*.jpg")
        self.assertIsNotNone(collectionWithDir)
        listOfFiles = listNameOfFiles(testDirectory, extension="jpg")
        self.assertIsNotNone(listOfFiles)
        listOfPaths = getFilePaths(testDirectory, listOfFiles)
        self.assertIsNotNone(listOfPaths)
        collectionWithPaths = imread_collection(listOfPaths)
        self.assertIsNotNone(collectionWithPaths)
        for image1 in collectionWithDir:
            for image2 in collectionWithPaths:
                equality = np.equal(collectionWithDir, collectionWithPaths)
                self.assertTrue(equality.all())

if __name__ == "__main__":
    envtest.main()
