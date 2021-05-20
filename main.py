from processImages import *

collectionDir = getCollectionDirectory()

leftEye = False

# To eventually implement with a tkinter interface.
# while True:
#     leftOrRightEye = input("Left or right eye?[L/R]")
#     if leftOrRightEye == "L":
#         leftEye = True
#         break
#     elif leftOrRightEye == "R":
#         break
#     else:
#         print("The input is invalid.")

grayImage = loadImages(collectionDir, leftEye=leftEye)
dataDictionary = seperateImages(grayImage, collectionDir)
dataDictionary = intensityCheck(dataDictionary)

image = dataDictionary["image"]
laser = dataDictionary["laserImage"]
xLaser = dataDictionary["xCenter"]
yLaser = dataDictionary["yCenter"]
rLaser = dataDictionary["radius"]
imageNumber = dataDictionary["imageNumber"]

indexShift = findImageShift(image)
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
