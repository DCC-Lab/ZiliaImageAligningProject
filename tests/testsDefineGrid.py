import envtest
from skimage.io import imread
from processImages import *

"""Incomplete, to finish later after improving shift detection."""

class TestDefineGrid(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testRandomImageIsLoaded(self):
        image = imread(self.testCV2CircleDirectory+"/blackImage.jpg")
        definedGrid = defineGrid(image)
        self.assertIsNotNone(definedGrid)

    def testTupleIsReturnedWithRandomImage(self):
        image = imread(self.testCV2CircleDirectory+"/blackImage.jpg")
        definedGrid = defineGrid(image)
        self.assertTrue(type(definedGrid) == tuple)

    def testElementsOfReturnedTupleAreIntegers(self):
        image = imread(self.testCV2CircleDirectory+"/blackImage.jpg")
        definedGrid = defineGrid(image)
        for element in definedGrid:
            self.assertTrue(type(element) == int)

    def testTheInputImageHasToHave3Dimensions(self):
        image = imread(self.testCV2CircleDirectory+"/blackImage.jpg")
        image = image[:,:,0]
        try:
            definedGrid = defineGrid(image)
            self.assertFalse(True)
        except IndexError:
            self.assertTrue(True)

    # def test3rdOutputArgumentIsTheLengthOfTheImage(self):
    #     # image = np.zeros((3,4,5))
    #     image = imread(self.testFilesDirectory+"/001-eye.jpg")
    #     definedGrid = defineGrid(image)
    #     # print(definedGrid[2])
    #     plt.imshow(drawGrid(image, definedGrid))
    #     plt.show()
    #     # self.assertTrue(definedGrid[2] == 5)





if __name__ == "__main__":
    envtest.main()