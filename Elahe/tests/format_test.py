import numpy as np
from skimage.io import imread_collection
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory

directory = askdirectory(title="Choose the folder containing the other modules.")
import sys
sys.path.insert(1, directory)
from processImages import *
from analyseRosaImages import *

M = np.array([[[0,0,1], [0,1,1], [1,0,1]], [[1,1,1], [1,1,1], [1,1,1]], [[1,1,1], [1,1,1], [1,1,1]]])

np.random.seed(1)
randomPicture = (np.random.rand(3,3,3)*255).astype(np.uint8)

plt.imshow(randomPicture)
plt.imsave("random3x3pic.png", randomPicture)
plt.show()

print(randomPicture)

# rng = np.random.default_rng(2021)
# print(rng.random(4))
# array([0.75694783, 0.94138187, 0.59246304, 0.31884171])

# print(M[0,:,:])



