import envtest
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
from skimage.data import coffee
from skimage.draw import ellipse_perimeter
from skimage.transform import hough_ellipse
from skimage.feature import canny
from skimage import color, img_as_ubyte
import time

class TestHoughEllipse(envtest.ZiliaTestCase):

    def plotEllipseResult(self, best, imageRgb, edges):
        # Code taken from an example in the scikit-image documentation.
        yc, xc, a, b = [int(round(x)) for x in best[1:5]]
        orientation = best[5]
        # Draw the ellipse on the original image
        cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
        imageRgb[cy, cx] = (0, 0, 255)
        # Draw the edge (white) and the resulting ellipse (red)
        edges = color.gray2rgb(img_as_ubyte(edges))
        edges[cy, cx] = (250, 0, 0)
        fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                        sharex=True, sharey=True)
        ax1.set_title('Original picture')
        ax1.imshow(imageRgb)
        ax2.set_title('Edge (white) and result (red)')
        ax2.imshow(edges)
        plt.show()

    # @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter50(self):
        # Default accuracy == 1. Let's try 50.
        startTime = time.time()
        imageRgb = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        xSize = grayImage.shape[0]
        ySize = grayImage.shape[1]
        minMajorAxis = int((1/6)*ySize)
        maxMinorAxis = int(0.5*xSize)
        houghResult = hough_ellipse(canniedImage, min_size=minMajorAxis,
            max_size=maxMinorAxis, accuracy=50)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 12.88 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Was pretty fast, and result looks pretty good, but not as much as 
        # accuracy 1...

if __name__ == "__main__":
    envtest.main()
