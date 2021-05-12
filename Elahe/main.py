from processImages import *

from tkinter.filedialog import askdirectory

collectionDir = askdirectory(title="Select the folder containing data")

# Initialize arrays
grayImage = np.array([])
Image = np.array([])
laser = np.array([])
xLaser = np.array([])
yLaser = np.array([])
rLaser = np.array([])

rightEye = True


grayImage = loadImages(collectionDir)
dataDictionary = seperateImages(grayImage, collectionDir)
dataDictionary = intensityCheck(dataDictionary)

image = dataDictionary["image"]
laser = dataDictionary["laserImage"]
xLaser = dataDictionary["xCenter"]
yLaser = dataDictionary["yCenter"]
rLaser = dataDictionary["radius"]
imageNumber = dataDictionary["imageNumber"]

indexShift = imageShift(image)
xRosa, yRosa = applyShift(xLaser, yLaser, indexShift)
xCenterGrid, yCenterGrid, length = defineGrid(image)
Label = placeRosa(xCenterGrid, yCenterGrid, length, xRosa, yRosa)
plotResult(image, length, xCenterGrid, yCenterGrid, xRosa, yRosa)

"""
for j in range(image.shape[0]):
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
    imageWithCircle = cv2.circle(image[0,:,:], center_coordinates, radius, color, thickness)
    #pyplot.imsave(str(3*j)+'.jpg', imageWithCircle)

    window_name = 'Image'
    center_coordinates = (int(xLaser[j]),int(yLaser[j]))
    radius = int(rLaser[j])
    # Blue color in BGR
    color = (0, 0, 255)
    # Line thickness of 2 px
    thickness = 5
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    imageWithCircle = cv2.circle(image[j,:,:], center_coordinates, radius, color, thickness)
    #pyplot.imsave(str(3*j+1)+'.jpg', imageWithCircle)

    imageWithCircle = cv2.circle(laser[j,:,:], center_coordinates, radius, color, thickness)
    #plt.imshow(image)
    #plt.show()
    #pyplot.imsave(str(3*j+2)+'.jpg', imageWithCircle)
"""
