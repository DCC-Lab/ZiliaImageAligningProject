import envtest
import cv2
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.feature import canny
from skimage.draw import ellipse
from skimage.exposure import adjust_gamma
import matplotlib.pyplot as plt
import numpy as np
from ellipse import LsqEllipse
from matplotlib.patches import Ellipse

class TestLsqEllipse(envtest.ZiliaTestCase):

    def testImportTestImage(self):
        testImage = self.testCannyDirectory+"/testPerfectBinaryEllipse.png"
        image = imread(testImage)
        self.assertIsNotNone(image)
        self.assertTrue(len(image.shape) == 3)

    def testImportGrayTestImage(self):
        testImage = self.testCannyDirectory+"/testPerfectBinaryEllipse.png"
        image = imread(testImage, as_gray=True)
        self.assertIsNotNone(image)
        self.assertTrue(len(image.shape) == 2)

    @envtest.skip("skip plots")
    def testThreshGrayEllipse(self):
        testImage = self.testCannyDirectory+"/testPerfectBinaryEllipse.png"
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image < thresh
        self.assertIsNotNone(image)
        self.assertTrue(len(binaryImage.shape) == 2)
        self.assertTrue(image.shape == binaryImage.shape)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(image, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(binaryImage, cmap="gray")
        plt.show()

    @envtest.skip("skip plots")
    def testThreshGrayRetina(self):
        testImage = self.testCannyDirectory+"/bresilMedium.jpg"
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        self.assertIsNotNone(image)
        self.assertTrue(len(binaryImage.shape) == 2)
        self.assertTrue(image.shape == binaryImage.shape)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(image, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(binaryImage, cmap="gray")
        plt.show()

    @envtest.skip("skip plots")
    def testCannyGrayEllipse(self):
        testImage = self.testCannyDirectory+"/testPerfectBinaryEllipse.png"
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image < thresh
        canniedImage = canny(binaryImage)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(image, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(canniedImage, cmap="gray")
        plt.show()

    @envtest.skip("skip plots")
    def testCannyGrayRetina(self):
        testImage = self.testCannyDirectory+"/bresilMedium.jpg"
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        canniedImage = canny(binaryImage)
        self.assertIsNotNone(canniedImage)
        self.assertTrue(image.shape == canniedImage.shape)
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(image, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(canniedImage, cmap="gray")
        plt.show()

    def testLSQEllipseImport(self):
        self.assertIsNotNone(LsqEllipse)

    @envtest.skip("skip plots and prints")
    def testLsqEllipse_HorizontalEllipseImage(self):
        # This test is directly based on the example found here:
        # https://github.com/bdhammel/least-squares-ellipse-fitting
        testImage = self.testCannyDirectory+"/testPerfectBinaryEllipse.png"
        colorImage = imread(testImage)
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        canniedImage = canny(binaryImage)

        # Get index pairs of the contours:
        X, Y = np.where(canniedImage == True)
        indexes = np.array(list(zip(X, Y)))
        # print(indexes)

        reg = LsqEllipse().fit(indexes)
        self.assertIsNotNone(reg)
        center, width, height, phi = reg.as_parameters()
        [yCenter, xCenter] = center
        print("center:", center) # [64.77547671811857, 112.93235984883405]
        print("width:", width) # 32.33031473568739 This is the vertical axis
        print("height:", height) # 53.940531246424094 this is the horizontal axis
        print("phi:", phi) # 0.00013424143672583532 this is almost == 0
        # I think the "width" is, in fact, the minor axis and the "height" is
        # the major axis (WRONG! See next tests)

        cy, cx = ellipse(int(yCenter), int(xCenter), int(width), int(height), rotation=phi)
        canniedImage[cy, cx] = 130
        image[cy, cx] = 255
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(canniedImage, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(colorImage)
        plt.show()

    @envtest.skip("skip plots and prints")
    def testLsqEllipse_VerticalEllipseImage(self):
        testImage = self.testStudentDirectory+"/testImage3.png"
        colorImage = imread(testImage)
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        canniedImage = canny(binaryImage)

        # Get index pairs of the contours:
        X, Y = np.where(canniedImage == True)
        indexes = np.array(list(zip(X, Y)))
        # print(indexes)

        reg = LsqEllipse().fit(indexes)
        self.assertIsNotNone(reg)
        center, width, height, phi = reg.as_parameters()
        [yCenter, xCenter] = center
        print("center:", center) # [82.3802224537652, 170.2780107167497]
        print("width:", width) # 41.1606929880854 This is the vertical axis
        print("height:", height) # 34.02078884419442 this is the horizontal axis
        print("phi:", phi) # 0.005528654260259732 this is almost == 0
        # It looks like "width" is the half length of the axis normal to the
        # angle. Height is the half length of the axis parallel to the angle.

        cy, cx = ellipse(int(yCenter), int(xCenter), int(width), int(height), rotation=phi)
        canniedImage[cy, cx] = 130
        image[cy, cx] = 255
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(canniedImage, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(colorImage)
        plt.show()

    @envtest.skip("skip plots and prints")
    def testLsqEllipse_AngledEllipseImage5(self):
        testImage = self.testStudentDirectory+"/testImage5.png"
        colorImage = imread(testImage)
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        canniedImage = canny(binaryImage)

        # Get index pairs of the contours:
        X, Y = np.where(canniedImage == True)
        indexes = np.array(list(zip(X, Y)))
        # print(indexes)

        reg = LsqEllipse().fit(indexes)
        self.assertIsNotNone(reg)
        center, width, height, phi = reg.as_parameters()
        [yCenter, xCenter] = center
        print("center:", center) # [46.792511360088255, 102.45029016530684]
        print("width:", width) # 24.409772295496847
        print("height:", height) # 48.72489440636081
        print("phi:", phi) # 0.36668821755544195
        # YES! It looks like "width" is the half length of the axis normal to
        # the angle. Height is the half length of the axis parallel to the angle.

        cy, cx = ellipse(int(yCenter), int(xCenter), int(width), int(height), rotation=phi)
        canniedImage[cy, cx] = 130
        image[cy, cx] = 255
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(canniedImage, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(colorImage)
        plt.show()

    @envtest.skip("skip plots and prints")
    def testLsqEllipse_AngledEllipseImage6(self):
        testImage = self.testStudentDirectory+"/testImage6.png"
        colorImage = imread(testImage)
        image = imread(testImage, as_gray=True)
        thresh = threshold_otsu(image)
        binaryImage = image > thresh
        canniedImage = canny(binaryImage)

        # Get index pairs of the contours:
        X, Y = np.where(canniedImage == True)
        indexes = np.array(list(zip(X, Y)))
        # print(indexes)

        reg = LsqEllipse().fit(indexes)
        self.assertIsNotNone(reg)
        center, width, height, phi = reg.as_parameters()
        [yCenter, xCenter] = center
        print("center:", center) # [72.74021686048583, 133.815298340835]
        print("width:", width) # 26.48914913767351
        print("height:", height) # 56.634102159997255
        print("phi:", phi) # -0.35672971896029765
        # YES YES! I confirm "width" is the half length of the axis normal to
        # the angle, and Height is the half length of the axis parallel to the
        # angle. I will have to rename them in the final code.
        # Also, the fact that the angle is negative tells me it most likely
        # ranges from -pi/2 to pi/2.

        cy, cx = ellipse(int(yCenter), int(xCenter), int(width), int(height), rotation=phi)
        canniedImage[cy, cx] = 130
        image[cy, cx] = 255
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(canniedImage, cmap="gray")
        plt.subplot(1,2,2)
        plt.imshow(colorImage)
        plt.show()

    @envtest.skip("skip plots")
    def testLsqEllipse_bresilMedium(self):
        testImage = self.testCannyDirectory+"/bresilMedium.jpg"

    @envtest.skip("skip plots")
    def testLsqEllipse_bresilHigh(self):
        testImage = self.testCannyDirectory+"/bresilHigh.jpg"

if __name__ == "__main__":
    envtest.main()
