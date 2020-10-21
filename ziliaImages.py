from utilities import findFiles, rearrangeChannels
from ImageAlignment import ImageAlignment
from skimage import io
import os
import numpy as np
import cv2


class ZiliaImages:
    def __init__(self):
        pass
        #self.dictImages = self.SortImages(os.path.normpath("C:\\zilia"))
        #self.directories = self.dictImages.keys()

    def sortRetinasAndRosas(self, imagePaths: list):
        # 0 for Blue, 1 for Green, 2 for Red :
        channel = 1
        means = []

        for imagePath in imagePaths:
            image = cv2.imread(imagePath, cv2.COLOR_BGR2GRAY)
            means.append(np.mean(image[:, :, channel]))

        meanOfMeans = np.mean(means)
        prevMean = meanOfMeans
        retinas = []
        rosas = []

        for mean, imagePath in zip(means, imagePaths):
            if mean > meanOfMeans:
                retinas.append(imagePath)
                #if prevMean > meanOfMeans:
                #    rosas.append(rosas[len(rosas) - 1])
            elif mean < meanOfMeans and prevMean < meanOfMeans:
                rosas.append(imagePath)
                retinas.append("None")
            else:
                rosas.append(imagePath)
            prevMean = mean

        return retinas, rosas
        '''
        # Get all the images mean values and read them.
        means = []
        images = []

        for imagePath in imagePaths:
            image = cv2.imread(imagePath, cv2.COLOR_BGR2GRAY)
            means.append(np.mean(image[:, :, 1]))
            images.append(cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2)))

        # Sort retinas and points using green channel
        mean = np.mean(means)
        previousMean = 999
        pts = []
        retinas = []

        ptsCSV = []
        retinasCSV = []
        n = 0
        for image in images:
            imgMean = np.mean(image[:, :, 2])
            if imgMean > mean:
                retinas.append(np.copy(image))
                retinasCSV.append(imagePaths[n])
            elif imgMean < mean and previousMean < mean:
                pts[len(pts) - 1] = np.copy(image)
                ptsCSV[len(ptsCSV) - 1] = imagePaths[n]
            else:
                ptsCSV.append(imagePaths[n])
                pts.append(image)
            previousMean = imgMean
            n += 1

        # Get rid of bad retina images and associated points using red channel
        # FIXME Needs to be tuned to get rid of really bad pictures.
        mean = 0
        for retina in retinas:
            mean += np.mean(retina[:, :, 2])
        mean = mean / len(retinas)

        n = 0
        for retina in retinas:
            if abs(np.mean(retina[:, :, 2]) - mean) / mean > 0.15:
                retinas.pop(n)
                pts.pop(n)
            n += 1

        return pts, retinas#, ptsCSV, retinasCSV
        '''

    '''
    def allignImages(self):
        # For "proof of concept". This is not exactly what we want to do.
        for directory in self.directories:
            print("Treatment of images in directory : ", directory)
            images = self.dictImages[directory]
            pts, imgs, ptsCSV, retinasCSV = self.sortRetinasAndRosas(images)
            print("Images succesfully sorted : ", len(pts), " points and ", len(imgs), " images.")

            with open(os.path.join(directory, 'sortedfiles.csv'), 'w') as file:
                file.write('points,retinas\n')
                for i in range(len(retinasCSV)):
                    string = '{},{}\n'.format(ptsCSV[i], retinasCSV[i])
                    file.write(string)

            # The first image in both lists are our references.
            ptRef = pts.pop(0)
            ref = imgs.pop(0)

            refShape = ref.shape
            zStack = np.zeros((len(imgs), refShape[0], refShape[1], refShape[2]), np.uint8)
            zStack[:, :512, :612, :] = cv2.resize(ref, (refShape[1] // 2, refShape[0] // 2))

            ia = ImageAlignment(cv2.resize(ref, (refShape[1], refShape[0])))
            ia.initiateSRReference()

            n = 0
            for img in imgs:
                ia.img = img
                zStack[n, 512:, :612, :] = cv2.resize(ia.img, (refShape[1] // 2, refShape[0] // 2))
                ia.setRegistration()
                ia.transform()
                zStack[n, 512:, 612:, :] = cv2.resize(ia.img, (refShape[1] // 2, refShape[0] // 2))

                ia.img = pts[n]
                ia.transform()
                zStack[n, :512, 612:, :] = cv2.resize(ia.img, (refShape[1] // 2, refShape[0] // 2))

                n += 1
                print("{}% completed.".format(int((n / len(imgs)) * 100)))

            stackPath = os.path.join(directory, "_stack.tiff")
            io.imsave(stackPath, zStack[:, :, :, ::-1])
            print("Saved stack image at : ", stackPath)
        '''
