import cv2
import numpy as np


class OrientedFASTRotatedBRIEF:
    def __init__(self, filter: np.ndarray, reference: np.ndarray, nFeatures=500):
        self.orb = cv2.ORB_create(nFeatures)
        self.matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

        # Reference image for ORB
        self.ref = reference
        self.kpRef, self.desRef = self.orb.detectAndCompute(filter, None)

        # Image to compare to the reference
        self.image = None
        self.kpImg = None
        self.desImg = None

    def keypointsAndDescriptors(self, image: np.ndarray):
        self.image = image
        self.kpImg, self.desImg = self.orb.detectAndCompute(image, None)

    def matchKeypoints(self):
        matches = self.matcher.match(self.desRef, self.desImg, None)
        return sorted(matches, key=lambda x: x.distance)

    def sortKeypoints(self, matches):
        src = np.zeros((len(matches), 2), dtype=np.float32)
        des = np.zeros((len(matches), 2), dtype=np.float32)
        for i, match in enumerate(matches):
            src[i, :] = self.kpRef[match.queryIdx].pt
            des[i, :] = self.kpImg[match.trainIdx].pt
        return src, des

    def findHomographyMatrix(self, source, destination):
        homography, mask = cv2.findHomography(source, destination, cv2.RANSAC)
        return homography, mask

    def applyHomography(self, homography, image=None):
        height = self.ref.shape[0]
        width = self.ref.shape[1]
        if image is None:
            return cv2.warpPerspective(self.image, homography, (width, height))
        else:
            return cv2.warpPerspective(image, homography, (width, height))

    def homography(self, filter: np.ndarray, image=None):
        self.keypointsAndDescriptors(filter)
        matches = self.matchKeypoints()
        src, des = self.sortKeypoints(matches)
        homography, mask = self.findHomographyMatrix(src, des)
        return self.applyHomography(homography, image)