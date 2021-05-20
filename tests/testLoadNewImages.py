import envtest
from processImages import *

oldFilesTestDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample"
newFilesTestDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"


class TestLoadNewImages(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportNewFiles(self):
        pass

    def testImportOldFiles(self):
        pass

    def testImportOldFilesDoesTheSameAsTheOldFunction(self):
        pass



if __name__ == "__main__":
    envtest.main()
