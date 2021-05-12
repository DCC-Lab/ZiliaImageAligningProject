import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory
directory = askdirectory(title="Choose the folder containing the other modules.")
import sys
sys.path.insert(1, directory)
from processImages import *
from analyseRosaImages import *

# M = np.array([[[0,0,1], [0,1,1], [1,0,1]], [[1,1,1], [1,1,1], [1,1,1]], [[1,1,1], [1,1,1], [1,1,1]]])
# print(M[0,:,:])

np.random.seed(1)
randomPicture1 = (np.random.rand(3,3,3)*255).astype(np.uint8)
np.random.seed(2)
randomPicture2 = (np.random.rand(3,3,3)*255).astype(np.uint8)
np.random.seed(3)
randomPicture3 = (np.random.rand(3,3,3)*255).astype(np.uint8)
np.random.seed(4)
randomPicture4 = (np.random.rand(3,3,3)*255).astype(np.uint8)

def showTheRandomPictures():
    plt.imshow(randomPicture1)
    plt.imsave("random3x3pic1.jpg", randomPicture1)
    plt.show()
    plt.imshow(randomPicture2)
    plt.imsave("random3x3pic2.jpg", randomPicture2)
    plt.show()
    plt.imshow(randomPicture3)
    plt.imsave("random3x3pic3.jpg", randomPicture3)
    plt.show()
    plt.imshow(randomPicture4)
    plt.imsave("random3x3pic4.jpg", randomPicture4)
    plt.show()

# showTheRandomPictures()

directory = getCollectionDirectory()
grayImage = loadImages(directory)
# first dimension has the same size as the number of images...
print(grayImage.shape)

plt.imshow(grayImage)
plt.show()
plt.imsave("grayImage.png", grayImage)

print(grayImage)

