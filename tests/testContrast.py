import envtest
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.exposure import is_low_contrast, adjust_gamma, adjust_log

class TestContrast(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)




if __name__ == "__main__":
    envtest.main()
