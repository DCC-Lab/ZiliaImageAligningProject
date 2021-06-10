import envtest
from skimage.io import imread
from processImages import *

class TestMirrorImage(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testImportTestImage(self):
        image = imread(self.testMirrorImageDirectory+"/testPic.jpg")
        self.assertIsNotNone(image)
        self.assertTrue(image.shape == (3,3,3))

    def testImageIsMirrored(self):
        image = imread(self.testMirrorImageDirectory+"/testPic.jpg")
        mirroredImage = mirrorImage(image)
        leftSideMirrored = np.equal(image[:,0,:], mirroredImage[:,2,:])
        rightSideMirrored = np.equal(image[:,2,:], mirroredImage[:,0,:])
        self.assertTrue(leftSideMirrored.all())
        self.assertTrue(rightSideMirrored.all())
        # plt.imshow(image)
        # plt.imshow(mirroredImage)
        # plt.show()




if __name__ == "__main__":
    envtest.main()
