import sys
import envtest
from processImages import *

testFilesDirectory = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\mini_test_sample_newdata"
# sys.path.insert(0, directory)


class TestFilterNewImages(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testFilesDirectoryIsAccessible(self):
        self.assertTrue(True)


# Ce que je veux faire, c'est m'assurer que les bons fichiers sont exclus, AUCUN AUTRE!!!



if __name__ == "__main__":
    envtest.main()
