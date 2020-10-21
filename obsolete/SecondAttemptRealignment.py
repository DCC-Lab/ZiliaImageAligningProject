import os
import cv2
import numpy as np
#import dcclab

currentPath = os.path.dirname(__file__)
imageFolder = os.path.join(currentPath, 'TestImages')


def getGradient(im):
    # Calculate the x and y gradients using Sobel operator
    grad_x = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=3)

    # Combine the two gradients
    grad = cv2.addWeighted(np.absolute(grad_x), 0.5, np.absolute(grad_y), 0.5, 0)
    return grad


# This attempt follows ExampleImageRealigning.py
if __name__ == '__main__':
    # First step is to load our reference :
    referencePath = os.path.join(imageFolder, '001.jpg')
    referenceOriginal = cv2.imread(referencePath, cv2.IMREAD_GRAYSCALE)

    # Load up the other images to use :
    imagePaths = [os.path.join(imageFolder, '003.jpg'), os.path.join(imageFolder, '005.jpg')]
    image1Original = cv2.imread(imagePaths[0], cv2.IMREAD_GRAYSCALE)

    sz = referenceOriginal.shape
    height = int(sz[0] / 3)
    width = sz[1]

    imageColor = np.zeros((height, width, 3), dtype=np.uint8)
    referenceColor = np.zeros((height, width, 3), dtype=np.uint8)
    mask = np.ones((height, width, 3), dtype=np.uint8)
    for i in range(3):
        imageColor[:, :, i] = image1Original[i * height:(i + 1) * height, :]
        referenceColor[:, :, i] = referenceOriginal[i * height:(i + 1) * height, :]

    alignedImage = np.zeros((height, width, 3), dtype=np.uint8)
    alignedImage = referenceColor[:, :, 2]

    warpMode = cv2.MOTION_HOMOGRAPHY
    warpMatrix = np.eye(3, 3, dtype=np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-10)

    for i in range(2) :
        (cc, warpMatrix) = cv2.findTransformECC(getGradient(referenceColor[:, :, i]), getGradient(imageColor[:, :, i]),
                                                warpMatrix, warpMode, criteria, mask, 5)

        if warpMode == cv2.MOTION_HOMOGRAPHY :
            # Use Perspective warp when the transformation is a Homography
            alignedImage[:,:,i] = cv2.warpPerspective(imageColor[:, :, i], warpMatrix, (width,height),
                                                      flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    cv2.imwrite(os.path.join(imageFolder, 'output2.jpg'), imageColor)
