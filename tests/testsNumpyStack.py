import envtest
import numpy as np
import matplotlib.pyplot as plt

class TestNumpyStack(envtest.ZiliaTestCase):

	def testInit(self):
		self.assertTrue(True)

	@envtest.skip("skip plots")
	def testMake2DImage(self):
		image = np.array([[135, 140],[240, 0]])
		self.assertIsNotNone(image)
		plt.imshow(image)
		plt.show()

	@envtest.expectedFailure
	def testMatplotlibDoesntAcceptImagesWith2ColorChannels(self):
		image = np.array([[135, 140],[240, 0]])
		image2 = np.array([[0, 0],[0, 255]])
		self.assertIsNotNone(image2)
		finalImage = np.stack((image, image2), axis=2)
		plt.imshow(finalImage)

	# @envtest.skip("skip plots")
	def testDStackInstead(self):
		image = np.array([[135, 140],[240, 0]])
		image2 = np.array([[0, 0],[0, 255]])
		self.assertIsNotNone(image2)
		finalImage = np.dstack((image, image, image2))
		print(finalImage.shape)
		plt.imshow(finalImage)
		plt.show()



if __name__ == "__main__":
	envtest.main()
