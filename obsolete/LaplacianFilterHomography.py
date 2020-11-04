import cv2
import numpy as np


# In this file we test a Laplacian filter.
# This is to do edge detection on our images. Then, using homography, we can brute force match the images.

# First step : Read the images and import into Grayscale
img1 = cv2.imread("../tests/TestImages/001.jpg")
img2 = cv2.imread("../tests/TestImages/003.jpg")
print(img1.shape, img2.shape)

# We apply the Laplacian filter next :
# Parameters are :
lap1 = cv2.Laplacian(img1, cv2.CV_8U, ksize=15)
lap2 = cv2.Laplacian(img2, cv2.CV_8U, ksize=15)

# Images are black. A possible fix? # FIXME
#lap1 = lap1 / lap1.max()
#lap2 = lap2 / lap2.max()
print(lap1.max(), lap1.min())

# Images are saved, again, for analysis purpose.
cv2.imwrite("../tests/TestImages/LaplacianFilter/LapFilter1.jpg", lap1)
cv2.imwrite("../tests/TestImages/LaplacianFilter/LapFilter2.jpg", lap2)

# We process the Homography.
# First we create an ORB object for detection.
orb = cv2.ORB_create(500, nlevels=32, edgeThreshold=31, patchSize=31, fastThreshold=10)
#orb = cv2.ORB_create(500)

# Using the ORB method, we find keypoints.
kp1, des1 = orb.detectAndCompute(lap1, None)
kp2, des2 = orb.detectAndCompute(lap2, None)
print(len(kp1), len(kp2))

# This is to visualize keypoints.
kpImg1 = cv2.drawKeypoints(img1, kp1, None, flags=None)
kpImg2 = cv2.drawKeypoints(img2, kp2, None, flags=None)
cv2.imwrite('../tests/TestImages/LaplacianFilter/kpImg1.jpg', kpImg1)
cv2.imwrite('../tests/TestImages/LaplacianFilter/kpImg2.jpg', kpImg2)

# Matching keypoints using Brute Force and sorting.
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
matches = matcher.match(des1, des2, None)
matches = sorted(matches, key=lambda x: x.distance)

# Visualize matches.
matchImg = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
cv2.imwrite('../tests/TestImages/LaplacianFilter/matchImg.jpg', matchImg)

# Getting rid of bad keypoints.
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    points2[i, :] = kp2[match.trainIdx].pt

print(len(points1), len(points2))

# Now, we can do the homography :
h, mask = cv2.findHomography(points1[:20], points2[:20], cv2.RANSAC)

# Using the homography
try:
    height, width, channel = img1.shape
except ValueError:
    height, width = img1.shape

img2Reg = cv2.warpPerspective(img2, h, (width, height))

# Results
cv2.imwrite('../tests/TestImages/LaplacianFilter/homography.jpg', img2Reg)