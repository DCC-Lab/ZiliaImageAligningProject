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

    def testInit(self):
        self.assertTrue(True)

    def testCoffee(self):
        image = coffee()
        self.assertIsNotNone(image)
        # plt.imshow(image)
        # plt.show()

    def testCropCoffee(self):
        image = coffee()[0:220, 160:420]
        self.assertIsNotNone(image)
        # plt.imshow(image)
        # plt.show()

    def testGrayscaleCoffee(self):
        image = coffee()
        grayImage = rgb2gray(image)
        self.assertIsNotNone(grayImage)
        # plt.imshow(grayImage, cmap=plt.cm.gray)
        # plt.show()

    def testOtsuThreshOnCoffee(self):
        image = coffee()
        grayImage = rgb2gray(image)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertIsNotNone(binaryImage)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()
        # Pretty bad, might not be a good reference for what we want to do
        # because there are much more color intensitites than in the
        # retina images...

    def testImreadGrayscaleOption(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        self.assertIsNotNone(grayImage)
        self.assertTrue(len(grayImage.shape) == 2)

    def testDifferentGrayscaleMethods(self):
        image = imread(self.testCannyDirectory+"/kenyaMedium.jpg")
        grayImage1 = rgb2gray(image)
        grayImage2 = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        equality = np.equal(grayImage1, grayImage2)
        self.assertTrue(equality.all())

    def testOtsuThreshOnMidLightRetina(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        self.assertIsNotNone(binaryImage)
        # plt.imshow(binaryImage, cmap=plt.cm.gray)
        # plt.show()

    def testOtsuThreshAndCanntOnMidLightRetina(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        self.assertIsNotNone(canniedImage)
        # plt.imshow(canniedImage, cmap=plt.cm.gray)
        # plt.show()
        # Very good :)

    @envtest.skip("Way too long, about 157 seconds! I'll change default parameters to optimize.")
    def testHoughEllipseDefaultParameters(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        cannied = canny(binaryImage)
        houghResults = hough_ellipse(cannied)
        # plt.imshow(cannied, cmap=plt.cm.gray)
        # plt.show()
        # houghResults.sort(order="accumulator")

    def testImageShape(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        shape = grayImage.shape
        self.assertIsNotNone(shape)
        self.assertTrue(len(shape) == 2)
        self.assertTrue(shape[0] < shape[1])
        # So the first dimension is the height,
        # and the second one is the width.

    @envtest.skip("Still too long, but about 60 seconds shorter than without ellipse parameter!")
    def testHoughEllipseWithChosenEllipseParameters(self):
        grayImage = imread(self.testCannyDirectory+"/kenyaMedium.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        xSize = grayImage.shape[0]
        ySize = grayImage.shape[1]
        minMajorAxis = int((1/6)*ySize)
        maxMinorAxis = int(0.5*xSize)
        houghResults = hough_ellipse(canniedImage, min_size=minMajorAxis, max_size=maxMinorAxis)

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

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter100(self):
        # Default accuracy == 1. Let's try 100, which should be extremely high.
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
            max_size=maxMinorAxis, accuracy=100)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # this test barely took about 14 seconds, but the result looks
        # like a straight line, which is very bad.

    @envtest.skip("Skip the plots and the calculating time.")
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

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter75(self):
        # Default accuracy == 1. Let's try 75.
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
            max_size=maxMinorAxis, accuracy=75)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Looks like a circle.

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter85(self):
        # Trying to find the limit before it becomes a straight line.
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
            max_size=maxMinorAxis, accuracy=85)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Looks like a circle.

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter90(self):
        # Trying to find the limit before it becomes a straight line.
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
            max_size=maxMinorAxis, accuracy=90)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Looks like a line, beurk.

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter60(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=60)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime) # 12.9 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Is too close to a circle

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter40(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=40)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime) # 12.97 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # less good than 50...

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter30(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=30)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 13.14 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # much better than 40!

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter20(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=20)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 13.26 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # better than 30!

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter10(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=10)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 14.42 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # very good

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter5(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=5)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 16.82 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # looks like a circle... very bad... why, though???

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter3(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=3)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 22.48 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Another ugly circle... ok... bad...

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter2(self):
        # Test lower limits to the algorithm
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
            max_size=maxMinorAxis, accuracy=2)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 33.55 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Another ugly circle... ok... bad...

    @envtest.skip("Skip the plots and the calculating time.")
    def testAccuracyParameter1(self):
        # This is supposed to be the default value.
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
            max_size=maxMinorAxis, accuracy=1)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 92.85 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Yup! Like default values, not faster at all!


    @envtest.skip("Wayyyyy too long, never finishes....")
    def testHighLightPictureRwandaHighDefaultThreshold(self):
        # Default accuracy == 1. Let's try 50.
        startTime = time.time()
        imageRgb = imread(self.testCannyDirectory+"/rwandaHigh.jpg")
        grayImage = imread(self.testCannyDirectory+"/rwandaHigh.jpg", as_gray=True)
        thresh = threshold_otsu(grayImage)
        binaryImage = grayImage > thresh
        canniedImage = canny(binaryImage)
        xSize = grayImage.shape[0]
        ySize = grayImage.shape[1]
        minMajorAxis = int((1/6)*ySize)
        maxMinorAxis = int(0.5*xSize)
        houghResult = hough_ellipse(canniedImage, min_size=minMajorAxis,
            max_size=maxMinorAxis, accuracy=100)
        houghResult.sort(order='accumulator')
        # Estimated parameters for the ellipse
        best = list(houghResult[-1])
        totalAlgorithmTime = time.time() - startTime
        print(totalAlgorithmTime)# 12.88 s
        self.plotEllipseResult(best, imageRgb, canniedImage)
        # Way too long... I never got it to even finish...

if __name__ == "__main__":
    envtest.main()
