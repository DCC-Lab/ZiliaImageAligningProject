import envtest
from processImages import *
import numpy as np

class TestNumpySort(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testSortedTestFile(self):
        directory = self.testFilesDirectory
        listFiles = listFileNames(directory)
        self.assertIsNotNone(listFiles)
        sort = np.sort(listFiles)
        self.assertIsNotNone
        # print(sort)
        # priotity on "-" before ".".


if __name__ == "__main__":
    envtest.main()
