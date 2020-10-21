import os
import cv2
import numpy as np
#import dcclab

currentPath = os.path.dirname(__file__)
imageFolder = os.path.join(currentPath, 'TestImages')


# This Attempt follows ExampleImageRegistration.py
if __name__ == '__main__':
    # First step is to load our reference :
    referencePath = os.path.join(imageFolder, '001.jpg')
    referenceOriginal = cv2.imread(referencePath)
    #cv2.imshow('Reference Original', referenceOriginal)
    #cv2.waitKey()
    #print(referenceOriginal.shape)

    # Load up the other images to use :
    imagePaths = [os.path.join(imageFolder, '003.jpg'), os.path.join(imageFolder, '005.jpg')]
    image1Original = cv2.imread(imagePaths[0])
    #cv2.imshow('First Image', image1Original)
    #cv2.waitKey()
    #print(image1Original.shape)

    # Convert to Grayscale.
    reference = cv2.cvtColor(referenceOriginal, cv2.COLOR_BGR2GRAY)
    image1 = cv2.cvtColor(image1Original, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray Reference', reference)
    #cv2.waitKey()
    #cv2.imshow('Gray Image', image1)
    #cv2.waitKey()
    #print(reference.shape, image1.shape)

    ''' By Default, we can't generate enough points with the ORB_create method.
    This means that we don't have enough points to do a Homography.
    We try different things :
    More Points, Thresholding, deblurring.
    
    ISSUE : Thresholding messes up the channels, which messes up the matching.
    '''
    # Threshold options are : THRESH_TOZERO, THRESH_TRUNC, THRESH_BINARY, THRESH_BINARY_INV, THRESH_MASK,
    # THRESH_OTSU, THRESH_TOZERO_INV, THRESH_TRIANGLE
    #ret, reference = cv2.threshold(reference, 125, 255, cv2.THRESH_TOZERO)
    #ret, image1 = cv2.threshold(image1, 125, 255, cv2.THRESH_TOZERO)
    #cv2.imwrite(os.path.join(imageFolder, 'ThreshRef.jpg'), reference)
    #cv2.imwrite(os.path.join(imageFolder, 'ThreshImg.jpg'), image1)

    ''' There are different techniques to do brute force matching. CV2 offers ORB, SIFT Radio Test and SIFT FLANN.
    So far ; ORB doesn't seem to give enough points for a RANSAC homography.
    '''
    # We use ORB to register features in our image :
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(reference, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image1, None)

    print('Keypoints for ref :', len(keypoints1), '| Descriptors for ref :', len(descriptors1))
    print('Keypoints for img :', len(keypoints2), '| Descriptors for img :', len(descriptors2))

    # We match the features :
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    print('Number of matches :', len(matches))

    # We can then sort matches by score and remove bad matches :
    # 0.15 is the percent for bad matches.
    matches.sort(key=lambda x: x.distance, reverse=False)
    numGoodMatches = int(len(matches) * 0.15)
    print('Number of good matches :', numGoodMatches)
    matches = matches[:numGoodMatches]

    # Afterwards, we draw top matches.
    imMatches = cv2.drawMatches(reference, keypoints1, image1, keypoints2, matches, None)
    cv2.imwrite(os.path.join(imageFolder, "matches.jpg"), imMatches)

    # Then, we have to extract the location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # We find the homography of the images :
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # We use the homography of the images :
    height, width, channels = image1.shape
    im1Reg = cv2.warpPerspective(reference, h, (width, height))

    #return im1Reg, h

    # We can then output the correct realigned image :
    cv2.imwrite(os.path.join(imageFolder, 'output.jpg'), im1Reg)

    # And get the homography estimate :
    print("Estimated Homography :", h)

    pass
