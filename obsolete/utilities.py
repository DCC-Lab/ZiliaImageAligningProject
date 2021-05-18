import os
import fnmatch
import numpy as np


def findFiles(directory, extension):
    foundFiles = []
    for root, directories, files in os.walk(os.path.normpath(directory)):
        for file in files:
            if fnmatch.fnmatch(file, extension):
                foundFiles.append(os.path.join(root, file))
    return foundFiles


def rearrangeChannels(image: np.ndarray, type='BGR2RGB'):
    newImage = np.zeros(image.shape, np.uint8)

    if type == 'BGR2RGB':
        newImage = image[:, :, ::-1]

    return newImage
