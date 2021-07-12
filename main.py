from processImages import *

# collectionDir = getCollectionDirectory()

# New data:
# collectionDir = r"./tests/TestImages/miniTestSampleNewData"

# Backup USB on Mac OS:
# collectionDir = r"/Volumes/DATA BACKUP/Baseline3/Bresil 1511184/20210316-100153-bresil-od-onh-rlp6"

# More new data that looks half decent...:
# collectionDir = r"E:\Baseline3\Kenya\20210316-144549-kenya-os-onh-rlp6-20210525T141349Z-001\20210316-144549-kenya-os-onh-rlp6"

# More new data that looks bad:
# collectionDir = r"E:\Baseline3\Kenya\20210316-141909-kenya-od-onh-rlp2-20210525T144923Z-001\20210316-141909-kenya-od-onh-rlp2"

# Partial new data that looks ok:
# collectionDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\sampleFromBaseline3"

# 521 files:
# collectionDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\20210316-144549-kenya-os-onh-rlp6"

# Broken test dir:
collectionDir = r"C:\Users\elm77\OneDrive\Documents\ULaval\2021_2_Ete\CERVO\Projet\code\brokenTest"


leftEye = False
newImages = True

grayImage = loadImages(collectionDir, leftEye=leftEye, newImages=newImages)
# dataDictionary = seperateImages(grayImage, collectionDir)
dataDictionary = seperateNewImages(grayImage, collectionDir)
dataDictionary = removeBadImages(dataDictionary)

image = dataDictionary["image"]
laser = dataDictionary["laserImage"]
xLaser = dataDictionary["xCenter"]
yLaser = dataDictionary["yCenter"]
rLaser = dataDictionary["radius"]
imageNumber = dataDictionary["imageNumber"]

indexShift = findImageShift(image)
shiftParameters = applyShift(xLaser, yLaser, indexShift)
gridParameters = defineGrid(image)

Label, dataDictionary, indexesToRemove = placeRosa(gridParameters, shiftParameters, dataDictionary)
# print(Label)
# print(dataDictionary["imageNumber"])

shiftParameters = cleanShiftParameters(shiftParameters, indexesToRemove)

shiftParameters = shiftParameters[0][:3], shiftParameters[1][:3]

newPlotResult(image, shiftParameters, gridParameters)
oldPlotResult(image, shiftParameters, gridParameters)
