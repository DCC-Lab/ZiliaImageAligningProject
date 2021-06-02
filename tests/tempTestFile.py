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

class TestHoughEllipse(envtest.ZiliaTestCase):

    def testHoughEllipseWithChosenEllipseParameters(self):
        image_rgb = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        xSize = grayImage.shape[0]
        ySize = grayImage.shape[1]
        minMajorAxis = int((1/6)*ySize)
        maxMinorAxis = int(0.5*xSize)
        houghResult = hough_ellipse(canniedImage, min_size=minMajorAxis, max_size=maxMinorAxis)
        houghResult.sort(order='accumulator')

        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        yc, xc, a, b = [int(round(x)) for x in best[1:5]]
        orientation = best[5]

        # Draw the ellipse on the original image
        cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
        image_rgb[cy, cx] = (0, 0, 255)
        # Draw the edge (white) and the resulting ellipse (red)
        edges = color.gray2rgb(img_as_ubyte(canniedImage))
        edges[cy, cx] = (250, 0, 0)

        fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True)

        ax1.set_title('Original picture')
        ax1.imshow(image_rgb)

        ax2.set_title('Edge (white) and result (red)')
        ax2.imshow(edges)

        plt.show()

        # plt.imshow(cannied, cmap=plt.cm.gray)
        # plt.show()


if __name__ == "__main__":
    envtest.main()
