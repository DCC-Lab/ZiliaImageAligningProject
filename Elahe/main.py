from functions1 import *
from functions2 import *

from tkinter.filedialog import askdirectory

collectionDir = askdirectory(title="Select the folder containing data")

# Initialize arrays
grayImage = np.array([])
Image = np.array([])
laser = np.array([])
xLaser = np.array([])
yLaser = np.array([])
rLaser = np.array([])

grayImage = loadImages(collectionDir)
Image, laser, xLaser, yLaser, rLaser, imageNumber = seperateImages(grayImage, collectionDir)
Image, laser, xLaser, yLaser, rLaser, imageNumber = intensityCheck(Image, laser, xLaser, yLaser, rLaser, imageNumber)
indexShift = imageShift(Image)
xRosa, yRosa = applyShift(xLaser, yLaser, indexShift)
xCenterGrid, yCenterGrid, length = defineGrid(Image)
Label = placeRosa(xCenterGrid, yCenterGrid, length, xRosa, yRosa)
plotResult(Image, length, xCenterGrid, yCenterGrid, xRosa, yRosa)

for j in range(Image.shape[0]):
    window_name = 'Image'
    # center_coordinates = (1000-int(indexShift[j,1]),1000-int(indexShift[j,0]))
    center_coordinates = (int(xRosa[j]), int(yRosa[j]))
    radius = 30
    # Blue color in BGR
    color = (0, 255, 0)
    # Line thickness of 2 px
    thickness = 5
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image = cv2.circle(Image[0,:,:], center_coordinates, radius, color, thickness)
    #pyplot.imsave(str(3*j)+'.jpg', image)
    
    
    window_name = 'Image'
    center_coordinates = (int(xLaser[j]),int(yLaser[j]))
    radius = int(rLaser[j])
    # Blue color in BGR
    color = (0, 0, 255)
    # Line thickness of 2 px
    thickness = 5
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image = cv2.circle(Image[j,:,:], center_coordinates, radius, color, thickness)
    #pyplot.imsave(str(3*j+1)+'.jpg',image)
    
    image = cv2.circle(laser[j,:,:], center_coordinates, radius, color, thickness)
    #plt.imshow(image)
    #plt.show()
    #pyplot.imsave(str(3*j+2)+'.jpg', image)
