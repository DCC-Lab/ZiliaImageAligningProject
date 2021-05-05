"""
This module has the following functions:
- loadImages(collectionDir)
- intensityCheck(Image,laser,xLaser,yLaser,rLaser,imageNumber)
- seperateImages(grayImageCollection,collectionDir)
- cross_image(im1, im2)
- ImageShift(Image)
- applyShift(xLaser,yLaser,shift)
- defineGrid(Image)
- placeRosa(xCenterGrid,yCenterGrid,length,xRosa,yRosa)
- plotResult (Image,length,xCenterGrid,yCenterGrid,xRosa,yRosa)

"""

from functions1 import *

from skimage.io import imread_collection
from skimage.color import rgb2gray
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import scipy.fftpack as fp
from matplotlib import pyplot
from scipy.signal import find_peaks
from scipy import ndimage
import scipy.signal


def loadImages(collectionDir):
    """
    This function get the directory of a series of images
    blue channel of the image = 0
    output is a series of grayscale images
    """
    collectionDir=collectionDir+'/*.jpg'
    imageCollection = imread_collection(collectionDir)
    grayImage=np.zeros((len(imageCollection),imageCollection[0].shape[0],imageCollection[0].shape[1]))
    for i in range(len(imageCollection)):
        imageCollection[i][:,:,2]=0
        grayImage[i,:,:]=rgb2gray(imageCollection[i])
    return grayImage



def intensityCheck(Image,laser,xLaser,yLaser,rLaser,imageNumber):
    """
    Purpose: remove images with low contrast or blurry
    1- use laplacian filter to remove blury images
    2- use average intensity in retinal images for thresholding
    input: series of retina images, series of rosa images, x,y, radius of the rosa center,
           image number in the original folder
    output: reduced data
    """
    
    index=np.array([])
    ii=np.array([])
    for kk in range(Image.shape[0]):
        d1=Image[kk,:,:]
        d1=256*((d1-np.min(d1))/(np.max(d1)-np.min(d1)))
        resLap = cv2.Laplacian(d1, cv2.CV_64F)
        score = resLap.var()
        ii=np.hstack((ii,score))
    T=np.mean(ii)
    index=np.where(ii>T)
    Image=np.delete(Image,index,axis=0)
    laser=np.delete(laser,index,axis=0)
    xLaser=np.delete(xLaser,index,axis=0)
    yLaser=np.delete(yLaser,index,axis=0)
    rLaser=np.delete(rLaser,index,axis=0)
    imageNumber=np.delete(imageNumber,index,axis=0)
    return Image,laser,xLaser,yLaser,rLaser,imageNumber



def seperateImages(grayImageCollection,collectionDir):
    """
    Purpose: seperate retina images from rosa images
    load retina image - then load the corresponding rosa image 
    check to find the rosa, if found, append the image and other info a the numpy array
    input: grayscale images (output of loadImages function), directory for the images folder
    output: numpy arrays including: retina images, rosa images,
            x,y, and radius of rosa center, number of the images in the directory
    """

    Thresh=np.mean(grayImageCollection)
    counter=0
    Image=np.empty((1,grayImageCollection.shape[1], grayImageCollection.shape[2]), float)
    laserImage=np.empty((1,grayImageCollection.shape[1], grayImageCollection.shape[2]), float)
    temp=np.empty((1, grayImageCollection.shape[1], grayImageCollection.shape[2]), float) # Emile modified 2nd argument
    xCenter=np.array([])
    yCenter=np.array([])
    radius=np.array([])
    imageNumber=np.array([])
    
    for i in range(0, grayImageCollection.shape[0]): # Emile changed first ind to 0 instead of 1
        print(f"Hello {i}")
        if (np.mean(grayImageCollection[i-1,:,:]) > Thresh and np.mean(grayImageCollection[i,:,:]) < Thresh):
            print(f"Hello first if worked, {i}")
            if (i<10):
                print(f"Hello < 10, {i}")
                loadLaserImage=collectionDir+'/00'+str(i)+'.jpg'
            if (i>=9 and i<100):
                print(f"Hello >= 10, {i}")
                loadLaserImage=collectionDir+'/0'+str(i)+'.jpg'
            if (i>=100):
                print(f"Hello >= 100, {i}")
                loadLaserImage=collectionDir+"/"+str(i)+'.jpg'
            print(loadLaserImage)
            blob = mainRosa(loadLaserImage)
            if (blob['found'] == True):
                print(f"Hello found true, {i}")
                temp[0,:,:]=grayImageCollection[i-1,:,:]
                Image=np.vstack((Image,temp))
                temp[0,:,:]=grayImageCollection[i,:,:]
                laserImage=np.vstack((laserImage,temp))

                xCenter=np.hstack((xCenter,int(blob['center']['x']*Image.shape[2])))
                yCenter=np.hstack((yCenter,int(blob['center']['y']*Image.shape[1])))
                radius=np.hstack((radius,int(blob['radius']*Image.shape[1])))
                imageNumber=np.hstack((imageNumber,int(i-1)))

    Image=np.delete(Image,0,axis=0)
    laserImage=np.delete(laserImage,0,axis=0)
    return Image,laserImage,xCenter,yCenter,radius,imageNumber



def cross_image(im1, im2):
    """
    calculate the cross correlation between two images
    get rid of the averages, otherwise the results are not good
    input: two 2D numpy arrays
    output: cross correlation
    """
    im1 -= np.mean(im1)
    im2 -= np.mean(im2)
    return scipy.signal.fftconvolve(im1, im2[::-1,::-1], mode='same')

def ImageShift(Image):
    """
    calculated the shift in x and y direction in two consecutive images
    input: 3D numpy array (series of retina images)
    the shift in the first image is considered to be zero
    output: 2D numpy array with the shifts in each image regarding the first image
    """

    Margin=250
    N=100
    temp=Image[:,Margin:Image.shape[1]-Margin,Margin:Image.shape[2]-Margin]
    skeletonImage=np.zeros(Image.shape)
    a=np.zeros(Image.shape)
    indexShift=np.array([0,0])
    totalShift=np.array([0,0])
    for j in range(temp.shape[0]):
        for i in range(temp.shape[1]):
            y=np.convolve(temp[j,i,:], np.ones(N)/N, mode='valid')
            peaks, properties = find_peaks(-y,prominence=0.001,distance=250)
            skeletonImage[j,i+Margin,peaks+Margin]=1
        for i in range(temp.shape[2]):
            y=np.convolve(temp[j,:,i], np.ones(N)/N, mode='valid')
            peaks, properties = find_peaks(-y,prominence=0.001,distance=250)
            skeletonImage[j,peaks+Margin,i+Margin]=1

        a[j,:,:]=ndimage.binary_closing(skeletonImage[j,:,:], structure=np.ones((20,20))).astype(np.int)
        
        if (j>0):
            out1=cross_image(a[j-1,:,:],a[j,:,:])
            ind= np.unravel_index(np.argmax(out1, axis=None), out1.shape)
            indexShift=np.vstack((indexShift,np.array(ind)-np.array([a.shape[1]/2,a.shape[2]/2])))
            totalShift=np.vstack((totalShift,np.sum(indexShift,axis=0)))
    return totalShift

def applyShift(xLaser,yLaser,shift):
    """
    apply the shift value on the x and y of the rosa
    """
    
    return (xLaser-shift[:,1]),(yLaser-shift[:,0])

def defineGrid(Image):
    temp=np.zeros(Image.shape)
    temp[np.where(Image>=np.mean(Image)*1.9)]=1
    kernel = np.ones((5,5),np.uint8)
    openingTemp = cv2.morphologyEx(temp[0,:,:], cv2.MORPH_OPEN, kernel)
    nonZero=np.nonzero(openingTemp)
    upToDown=np.max(nonZero[0])-np.min(nonZero[0])
    rightToLeft=np.max(nonZero[1])-np.min(nonZero[1])
    upToDownCenter=int(((np.max(nonZero[0])+np.min(nonZero[0]))/2)-(upToDown-rightToLeft))
    rightToLeftCenter=int((np.max(nonZero[1])+np.min(nonZero[1]))/2)
    length=int((np.min([upToDown,rightToLeft]))/2)
    return rightToLeftCenter,upToDownCenter,length


def placeRosa(xCenterGrid,yCenterGrid,length,xRosa,yRosa):
    xLabel=np.array(['1','2','3','4','5','6','7','8','9','10'])
    yLabel=np.array(['A','B','C','D','E','F','J','K','L','M'])

    xGrid=np.array(range(-5*length,5*length))
    xlabel = np.array( ["" for x in range(xGrid.shape[0])])
    for x in range(xLabel.shape[0]):
        xlabel[x*length:(x+1)*length]=xLabel[x]
    yGrid=np.array(range(-5*length,5*length))
    ylabel = np.array( ["" for x in range(yGrid.shape[0])])
    for y in range(yLabel.shape[0]):
        ylabel[y*length:(y+1)*length]=yLabel[y]
    outputLabel=[]
    for j in range(xRosa.shape[0]):
        L=str(str(xlabel[(np.where(xGrid == xRosa[j]-xCenterGrid))[0]][0])+
                       str(ylabel[(np.where(yGrid == yRosa[j]-yCenterGrid))[0]][0]))
        outputLabel.append(L)
    return outputLabel


def plotResult (Image,length,xCenterGrid,yCenterGrid,xRosa,yRosa):
    for j in range(Image.shape[0]):
        window_name = 'Image'  
        center_coordinates = (int(xRosa[j]),int(yRosa[j]))
        radius = 30
        color = (0, 255, 0)
        thickness = 5
        image = cv2.circle(Image[0,:,:], center_coordinates, radius, color, thickness)
        left=np.max([xCenterGrid-(length*5),0])
        
    up=np.max([yCenterGrid-(length*5),0])
    right=np.min([(5*length),(Image.shape[1]-xCenterGrid)])+xCenterGrid
    down=right=np.min([(5*length),(Image.shape[2]-yCenterGrid)])+yCenterGrid
    temp=Image[0,up:down,left:right]
    xNewCenter=xCenterGrid-left
    yNewCenter=yCenterGrid-up
    gridImage=np.zeros([length*10,length*10])
    gridImage[((5*length)-yNewCenter):((5*length)+(temp.shape[0]-yNewCenter)),((5*length)-xNewCenter):((5*length)+(temp.shape[1]-xNewCenter))]=temp
    
    plt.figure()
    img=gridImage.copy()
    dx, dy = length,length

    # Custom (rgb) grid color
    grid_color = 0

    # Modify the image to include the grid
    img[:,::dy] = grid_color
    img[::dx,:] = grid_color

    plt.imshow(img)
    pyplot.imsave('Result.jpg',img)
