import numpy as np
import cv2


img1 = cv2.imread("../TestImages/001.jpg")
img2 = cv2.imread("../TestImages/003.jpg")
print(img1.shape, img2.shape)

blur1 = cv2.GaussianBlur(img1, (9, 9), 0)
blur2 = cv2.GaussianBlur(img2, (9, 9), 0)

# Sobel in x
sob1 = cv2.Sobel(blur1, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
sob2 = cv2.Sobel(blur2, cv2.CV_32F, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

cv2.imwrite("../TestImages/SobelXFilter/sob1X.jpg", sob1)
cv2.imwrite("../TestImages/SobelXFilter/sob2X.jpg", sob2)

# We process the Homography.
# First we create an ORB object for detection.
#orb = cv2.ORB_create(500, nlevels=32, edgeThreshold=60, patchSize=60)
orb = cv2.ORB_create(500)

# Using the ORB method, we find keypoints.
kp1, des1 = orb.detectAndCompute(sob1, None)
kp2, des2 = orb.detectAndCompute(sob2, None)
print(len(kp1), len(kp2))

# This is to visualize keypoints.
kpImg1 = cv2.drawKeypoints(img1, kp1, None, flags=None)
kpImg2 = cv2.drawKeypoints(img2, kp2, None, flags=None)
cv2.imwrite('../TestImages/SobelXFilter/kpImg1.jpg', kpImg1)
cv2.imwrite('../TestImages/SobelXFilter/kpImg2.jpg', kpImg2)

# Matching keypoints using Brute Force and sorting.
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
matches = matcher.match(des1, des2, None)
matches = sorted(matches, key=lambda x: x.distance)

# Visualize matches.
matchImg = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
cv2.imwrite('../TestImages/SobelXFilter/matchImg.jpg', matchImg)

# Getting rid of bad keypoints.
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    points2[i, :] = kp2[match.trainIdx].pt

print(len(points1), len(points2))

# Now, we can do the homography :
h, mask = cv2.findHomography(points1[:40], points2[:40], cv2.RANSAC)

# Using the homography
try:
    height, width, channel = img1.shape
except ValueError:
    height, width = img1.shape

img2Reg = cv2.warpPerspective(img2, h, (width, height))

# Results
cv2.imwrite('TestImages/SobelXFilter/homography.jpg', img2Reg)