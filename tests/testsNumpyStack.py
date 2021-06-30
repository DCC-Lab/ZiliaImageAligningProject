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

	def testStackAxis2(self):
		image = np.array([[135, 140],[240, 0]])
		image2 = np.array([[0, 0],[0, 255]])
		self.assertIsNotNone(image2)
		

if __name__ == "__main__":
	envtest.main()
