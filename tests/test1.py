import os
import numpy as np
from utilities import findFiles, rearrangeChannels
from ziliaImage.ImageAlignment import ImageAlignment
from skimage import io


if __name__ == '__main__':
    root = os.path.normpath("C:\\zilia\\jour4\\singe22\\oeilDroit_singe22\\150-150-150-50_psr")
    images = findFiles(root, '*.jpg')[:41]

    # Remove the first image, which is a point reference.
    # The second image is our reference for the homographies.
    pointRef = images.pop(0)
    retinaRef = images.pop(0)

    # Create the ImageAlignment object with the retinaRef as reference.
    alignment = ImageAlignment(retinaRef)

    # Setup variables for the z-stack.
    imShape = alignment.ref.shape
    zStack = np.zeros((len(images) // 2 + 1, imShape[0], imShape[1], imShape[2]), np.uint8)

    # Adding the reference at the front of the z-stack.
    zStack[0, :, :, :] = rearrangeChannels(alignment.ref)
    alignment.initiateSRReference()

    # We iterate through the images.
    for i in range(0, 19):
        alignment.readImage(images[(2 * i) + 1][1])
        alignment.setRegistration()
        alignment.transform()

        zStack[i + 1, :, :, :] = rearrangeChannels(alignment.img)

    # We save the zstack.
    stackPath = os.path.join(root, '_stack.tiff')
    io.imsave(stackPath, zStack)


