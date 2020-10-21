import numpy as np
import scipy.signal as signal
import cv2


def normalizedCrossCorrelate(ref, src):
    a = (ref - np.mean(ref)) / (np.std(ref) * np.size(ref))
    b = (src - np.mean(src)) / (np.std(src))
    return np.clip(signal.correlate2d(a, b, 'full') * 255, 0, 255).astype(np.uint8)


if __name__ == '__main__':
    ref = cv2.imread("../TestImages/001.jpg")
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

    src1 = cv2.imread("../TestImages/LoGFilter/homography.jpg")
    src2 = cv2.imread("../TestImages/LoGFilter/homography2.jpg")
    src1 = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)
    src2 = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY)

    corr1 = normalizedCrossCorrelate(ref[1250:1750, 1250:1750], src1[1250:1750, 1250:1750])
    corr2 = normalizedCrossCorrelate(ref[1250:1750, 1250:1750], src2[1250:1750, 1250:1750])

    cv2.imwrite("../TestImages/correlation/Corr1.jpg", corr1, )
    cv2.imwrite("../TestImages/correlation/Corr2.jpg", corr2)
