import numpy as np
from skimage.io import imread_collection
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

def loadImages(collectionDir: str) -> np.ndarray:
    """
    This function gets the directory of a series of images
    Blue channel of the image = 0
    Output is a series of grayscale images
    """
    collectionDir = collectionDir+'/*.jpg'
    imageCollection = imread_collection(collectionDir)# imports as RGB image
    print("Type of image collection = ", type(imageCollection))
    grayImage = np.zeros((len(imageCollection), imageCollection[0].shape[0],imageCollection[0].shape[1]))
    for i in range(len(imageCollection)):
        imageCollection[i][:,:,2] = 0
        grayImage[i,:,:] = rgb2gray(imageCollection[i])
    return grayImage


def seperateImages(grayImageCollection, collectionDir: str):
    """
    Purpose: seperate retina images from rosa images
    Load retina image - then load the corresponding rosa image 
    Check to find the rosa, if found, append the image and other info a the numpy array
    Input: grayscale images (output of loadImages function), directory for the images folder
    Output: dictionary including: retina images, rosa images,
            x,y, and radius of rosa center, numbers of the images in the directory
    """
    # 1st image has to be the retina, 2nd has to be the rosa.
    Thresh = np.mean(grayImageCollection)
    counter = 0
    image = np.empty((1, grayImageCollection.shape[1], grayImageCollection.shape[2]), float)
    laserImage = np.empty((1, grayImageCollection.shape[1], grayImageCollection.shape[2]), float)
    temp = np.empty((1, grayImageCollection.shape[1], grayImageCollection.shape[2]), float)
    xCenter = np.array([])
    yCenter = np.array([])
    radius = np.array([])
    imageNumber = np.array([])

    for i in range(1, grayImageCollection.shape[0]):
        if (np.mean(grayImageCollection[i-1,:,:]) > Thresh and np.mean(grayImageCollection[i,:,:]) < Thresh):
            if (i < 10):
                loadLaserImage = collectionDir+'/00'+str(i)+'.jpg'
            if (i >= 10 and i < 100):
                loadLaserImage = collectionDir+'/0'+str(i)+'.jpg'
            if (i >= 100):
                loadLaserImage = collectionDir+"/"+str(i)+'.jpg'
            blob = mainRosa(loadLaserImage)
            if (blob['found'] == True):
                temp[0,:,:] = grayImageCollection[i-1,:,:] # retina
                image = np.vstack((image, temp)) # retina
                temp[0,:,:] = grayImageCollection[i,:,:] # rosa
                laserImage = np.vstack((laserImage,temp)) # rosa

                # the following arrays are 1D
                xCenter = np.hstack((xCenter,int(blob['center']['x']*image.shape[2]))) # for the center of the rosa
                yCenter = np.hstack((yCenter,int(blob['center']['y']*image.shape[1]))) # for the center of the rosa
                radius = np.hstack((radius,int(blob['radius']*image.shape[1]))) # for the center of the rosa
                imageNumber = np.hstack((imageNumber,int(i-1))) # it's a 1D array

    image = np.delete(image,0,axis=0) # remove the first initialized empty matrix
    laserImage = np.delete(laserImage,0,axis=0) # remove the first initialized empty matrix
    dataDictionary = {
        "image": image,
        "laserImage": laserImage,
        "xCenter": xCenter,
        "yCenter": yCenter,
        "radius": radius,
        "imageNumber": imageNumber
    }
    return dataDictionary

M = np.array([[[0,0,1], [0,1,1], [1,0,1]], [[1,1,1], [1,1,1], [1,1,1]], [[1,1,1], [1,1,1], [1,1,1]]])


np.random.seed(1)
R = (np.random.rand(3,3,3)*255).astype(np.uint8)

plt.imshow(R)
plt.imsave("random3x3pic.png", R)
plt.show()

print(R)

# rng = np.random.default_rng(2021)
# print(rng.random(4))
# array([0.75694783, 0.94138187, 0.59246304, 0.31884171])

# print(M[0,:,:])



