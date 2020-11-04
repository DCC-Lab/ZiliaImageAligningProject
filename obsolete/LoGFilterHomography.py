import cv2
import numpy as np


def gaussBlur(source, sigmaX):
    return cv2.GaussianBlur(source, (0, 0), sigmaX)


def laplacian(source, kernelSize):
    return cv2.Laplacian(source, cv2.CV_8U, ksize=kernelSize)


def LoGFilter(source, sigmaX, kernelSize):
    return laplacian(gaussBlur(source, sigmaX), kernelSize)


# In this file we test a LoG filter. LoG stands for Laplacian of Gaussian.
# This is to do edge detection on our images. Then, using homography, we can brute force match the images.

# Image Channels are BGR

''' Parameters with an impact :
GaussianBlur Kernel Size : 
With SigmaX = 0, (3, 3) doesn't seem to be enough. (15, 15) is too much. (9, 9) works well.
With a larger SigmaX, like 9, it looks like we need a bigger kernel. It gives images with better edges but it doesn't 
    seem to help with the homography.
    It looks like the trick is to keep the kernel size to (0, 0) and have it computed from SigmaX. At which point, a 
    bigger gives a smoother blur and a better Laplacian.
    
ORB detection : nlevels=32, edgeThreshold=60, patchSize=60 works for [(3, 3), 0].

findHomography : We get a lot of points. How many is too little and how many is too much?
'''

# First step : Read the images and import into Grayscale
img1 = cv2.imread("../tests/TestImages/001.jpg")
img2 = cv2.imread("../tests/TestImages/003.jpg")
img3 = cv2.imread("../tests/TestImages/005.jpg")

copyImg1 = np.copy(img1)
copyImg2 = np.copy(img2)
copyImg3 = np.copy(img3)


blueChannel = np.zeros(img1.shape, dtype=int)
copyImg1[:, :, 0] = blueChannel[:, :, 0]
copyImg2[:, :, 0] = blueChannel[:, :, 0]
copyImg3[:, :, 0] = blueChannel[:, :, 0]

sigmaX = 15
kernelSize = 9

lap1 = LoGFilter(copyImg1[:, 200:2200, :], sigmaX, kernelSize)
lap2 = LoGFilter(copyImg2[:, 200:2200, :], sigmaX, kernelSize)
lap3 = LoGFilter(copyImg3[:, 200:2200, :], sigmaX, kernelSize)

# Images are saved, again, for analysis purpose.
cv2.imwrite("../tests/TestImages/LoGFilter/LapFilter1.jpg", lap1)
cv2.imwrite("../tests/TestImages/LoGFilter/LapFilter2.jpg", lap2)
cv2.imwrite("../tests/TestImages/LoGFilter/LapFilter3.jpg", lap3)

# We process the Homography.
# First we create an ORB object for detection.
orb = cv2.ORB_create(500)

# Using the ORB method, we find keypoints.
kp1, des1 = orb.detectAndCompute(lap1, None)
kp2, des2 = orb.detectAndCompute(lap2, None)
kp3, des3 = orb.detectAndCompute(lap3, None)
print(len(kp1), len(kp2), len(kp3))

# This is to visualize keypoints.
kpImg1 = cv2.drawKeypoints(img1, kp1, None, flags=None)
kpImg2 = cv2.drawKeypoints(img2, kp2, None, flags=None)
kpImg3 = cv2.drawKeypoints(img3, kp3, None, flags=None)
cv2.imwrite('../tests/TestImages/LoGFilter/kpImg1.jpg', kpImg1)
cv2.imwrite('../tests/TestImages/LoGFilter/kpImg2.jpg', kpImg2)
cv2.imwrite('../tests/TestImages/LoGFilter/kpImg3.jpg', kpImg3)

# Matching keypoints using Brute Force and sorting. # FIXME IMG2
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
matches = matcher.match(des1, des2, None)
matches = sorted(matches, key=lambda x: x.distance)
# Visualize matches.
matchImg = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
cv2.imwrite('../tests/TestImages/LoGFilter/matchImg.jpg', matchImg)

# Matching keypoints using Brute Force and sorting. # FIXME IMG3
matches2 = matcher.match(des1, des3, None)
matches2 = sorted(matches2, key=lambda x: x.distance)
# Visualize matches.
matchImg2 = cv2.drawMatches(img1, kp1, img2, kp2, matches2, None)
cv2.imwrite('../tests/TestImages/LoGFilter/matchImg2.jpg', matchImg2)

# Getting rid of bad keypoints. # FIXME IMG2
source = np.zeros((len(matches), 2), dtype=np.float32)
destination = np.zeros((len(matches), 2), dtype=np.float32)
for i, match in enumerate(matches):
    source[i, :] = kp1[match.queryIdx].pt
    destination[i, :] = kp2[match.trainIdx].pt
print(len(source), len(destination))
# Now, we can do the homography :
h, mask = cv2.findHomography(source[:10], destination[:10], cv2.RANSAC)

# Getting rid of bad keypoints. # FIXME IMG3
source = np.zeros((len(matches2), 2), dtype=np.float32)
destination = np.zeros((len(matches2), 2), dtype=np.float32)
for i, match in enumerate(matches2):
    source[i, :] = kp1[match.queryIdx].pt
    destination[i, :] = kp3[match.trainIdx].pt
print(len(source), len(destination))
# Now, we can do the homography :
h2, mask2 = cv2.findHomography(source[:10], destination[:10], cv2.RANSAC)

# Using the homography
try:
    height = img1.shape[0] #+ img2.shape[0]
    width = img1.shape[1] #+ img2.shape[1]
    channel = img1.shape[2]
except ValueError:
    height = img1.shape[0] #+ img2.shape[0]
    width = img1.shape[1] #+ img2.shape[1]

img2Reg = cv2.warpPerspective(img2, h, (width, height))
img3Reg = cv2.warpPerspective(img3, h2, (width, height))

# Results
cv2.imwrite('../tests/TestImages/LoGFilter/homography.jpg', img2Reg)
cv2.imwrite('../tests/TestImages/LoGFilter/homography2.jpg', img3Reg)
