import cv2


def gaussBlur(source, sigmaX):
    return cv2.GaussianBlur(source, (0, 0), sigmaX)


def laplacian(source, kernelSize):
    return cv2.Laplacian(source, cv2.CV_8U, ksize=kernelSize)


def LoGFilter(source, sigmaX, kernelSize):
    return laplacian(gaussBlur(source, sigmaX), kernelSize)