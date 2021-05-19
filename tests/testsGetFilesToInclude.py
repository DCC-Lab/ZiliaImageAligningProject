import envtest
from processImages import *

testFilesDirectory = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"

class TestGetFilesToInclude(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testTheRightFilesAreExcluded(self):
        includedFiles = getFilesToInclude(testFilesDirectory, extension="jpg")
        for imageName in includedFiles:
            if "eye" in imageName:
                self.assertFalse("rosa" in imageName.lower())
            if "rosa" in imageName:
                self.assertFalse("eye" in imageName.lower())


if __name__ == "__main__":
    envtest.main()
