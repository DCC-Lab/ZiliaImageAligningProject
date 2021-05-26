import envtest
from processImages import *

class TestGetFilesToInclude(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testTheRightFilesAreExcluded(self):
        includedFiles = getFilesToInclude(self.testFilesDirectory, extension="jpg")
        for imageName in includedFiles:
            if "eye" in imageName:
                self.assertFalse("rosa" in imageName.lower())
            if "rosa" in imageName:
                self.assertFalse("eye" in imageName.lower())


if __name__ == "__main__":
    envtest.main()
