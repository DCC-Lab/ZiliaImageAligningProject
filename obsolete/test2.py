from pystackreg import StackReg
import cv2
import numpy as np


if __name__ == '__main__':
    ref = cv2.imread("TestImages/001.jpg")
    refCopy = np.copy(ref)
    img = cv2.imread('TestImages/003.jpg')
    imgCopy = np.copy(img)

    # Crop
    ref = ref[180:2250, 160:1860, :]
    img = img[180:2250, 160:1860, :]

    # Register
    sr = StackReg(StackReg.AFFINE)
    sr.register(ref[:, :, 2], img[:, :, 2])

    # Transform
    newImg = np.zeros(refCopy.shape, dtype=int)
    for channel in range(refCopy.shape[2]):
        newImg[:, :, channel] = sr.transform(imgCopy[:, :, channel])

    cv2.imwrite("Test.jpg", newImg)

