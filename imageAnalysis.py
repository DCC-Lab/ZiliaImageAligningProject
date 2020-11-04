from ImageAlignment import ImageAlignment
#from rosa.find_rosa_dc import find_laser_spot_main_call
from rosa.find_rosa_dc_v2 import find_laser_spot_main_call
import rosa.find_rosa_dc_v2
import rosa.find_rosa_dc
from matplotlib import pyplot as plt
from skimage import io
import os
import numpy as np
import cv2
import sqlite3 as lite
import time


class ImageAnalysis:
    def __init__(self):
        self.retRef = None
        self.rosaRef = None
        self.rosaRefPos = None
        self.rosaRefRadius = None
        self.shapeRef = None
        #self.dictImages = self.SortImages(os.path.normpath("C:\\zilia"))
        #self.directories = self.dictImages.keys()

    def sortRetinasAndRosas(self, imagePaths: list):
        # TODO Move somewhere else. Not appropriate in this class.
        # 0 for Blue, 1 for Green, 2 for Red :
        channel = 2
        means = []

        for imagePath in imagePaths:
            image = cv2.imread(imagePath, cv2.COLOR_BGR2GRAY)
            means.append(np.mean(image[:, :, channel]))

        meanOfMeans = np.mean(means)
        retinas = []
        rosas = []
        prevImg = None

        for mean, imagePath in zip(means, imagePaths):
            if mean > meanOfMeans:
                retinas.append(imagePath)
                if prevImg == 'ret':
                    try:
                        rosas.append(rosas[len(rosas) - 1])
                    except:
                        rosas.append('None')
                prevImg = 'ret'
            elif mean < meanOfMeans:
                rosas.append(imagePath)
                if prevImg == 'rosa':
                    retinas.append("None")
                prevImg = 'rosa'
            else:
                print("Image {} could not be sorted...".format(imagePath))
                f = open('errors.txt', 'a')
                f.write('Error for {} at {}\n'.format(imagePath, time.time()))
                f.close()

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

    def setReferences(self, rows: lite.Row):
        # For now, the reference doesn't really need to be any specific image.
        # I skip the first couple of images and ignore the first couple of remaining images.
        i = np.random.randint((len(rows) // 10) * 5, (len(rows) // 10) * 6)
        print(rows[i]['retinas'], rows[i]['rosas'])
        self.retRef = cv2.imread(rows[i]['retinas'], cv2.COLOR_BGR2GRAY)
        self.rosaRef = cv2.imread(rows[i]['rosas'], cv2.COLOR_BGR2GRAY)
        self.shapeRef = self.retRef.shape
        self.rosaRefPos, self.rosaRefRadius = self.getRosaReferencePosition()

    def getRosaReferencePosition(self):
        blob, recTime, found = find_laser_spot_main_call(self.rosaRef)
        center = (int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0]))
        radius = int(blob['radius'] * self.shapeRef[0])
        return center, radius

    def findLaserSpot(self, img: np.ndarray):
        blob = rosa.find_rosa_dc.find_laser_spot_main_call(img)
        if self.shapeRef:
            center = (int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0]))
            radius = int(blob['radius'] * self.shapeRef[0])
        else:
            shape = img.shape
            center = (int(blob['center']['x'] * shape[1]), int(blob['center']['y'] * shape[0]))
            radius = int(blob['radius'] * shape[0])
        return center, radius

    def findLaserSpotV2(self, img: np.ndarray):
        blob, recTime, found = rosa.find_rosa_dc_v2.find_laser_spot_main_call(img)
        if self.shapeRef:
            center = (int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0]))
            radius = int(blob['radius'] * self.shapeRef[0])
        else:
            shape = img.shape
            center = (int(blob['center']['x'] * shape[1]), int(blob['center']['y'] * shape[0]))
            radius = int(blob['radius'] * shape[0])
        return center, radius

    def compareFindLaserSpotOneImage(self, img: np.ndarray, iter=100):
        x1s, y1s, r1s, x2s, y2s, r2s = [], [], [], [], [], []

        for i in range(iter):
            c1, r1 = self.findLaserSpot(img)
            c2, r2 = self.findLaserSpotV2(img)

            x1s.append(c1[0])
            y1s.append(c1[1])
            r1s.append(r1)

            x2s.append(c2[0])
            y2s.append(c2[1])
            r2s.append(r2)

        plt.imshow(img[:, :, ::-1])
        plt.scatter(x=x1s, y=y1s, s=r1s, facecolors='none', edgecolors='g')
        plt.scatter(x=x2s, y=y2s, s=r2s, facecolors='none', edgecolors='y')
        plt.show()

    def compareFindLaserSpotMultipleImages(self, rows: lite.Row):
        maxDistance = 200
        x1s, y1s, r1s, x2s, y2s, r2s = [], [], [], [], [], []
        dxs, dys, drs, axes = [], [], [], []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1 = self.findLaserSpot(img)
            c2, r2 = self.findLaserSpotV2(img)

            x1s.append(c1[0])
            x2s.append(c2[0])
            dxs.append(abs(c1[0] - c2[0]))

            y1s.append(c1[1])
            y2s.append(c2[1])
            dys.append(abs(c1[1] - c2[1]))

            r1s.append(r1)
            r2s.append(r2)
            drs.append(abs(r1 - r2))

            axes.append(n)

        plt.figure()
        plt.subplot(311)
        plt.plot(axes, x1s, 'r', label='X V1')
        plt.plot(axes, x2s, 'b', label='X V2')
        plt.plot(axes, dxs, 'g--', label='Delta X')
        plt.legend()

        plt.subplot(312)
        plt.plot(axes, y1s, 'r', label='Y V1')
        plt.plot(axes, y2s, 'b', label='Y V2')
        plt.plot(axes, dys, 'g--', label='Delta Y')
        plt.legend()

        plt.subplot(313)
        plt.plot(axes, r1s, 'r', label='R V1')
        plt.plot(axes, r2s, 'b', label='R V2')
        plt.plot(axes, drs, 'g--', label='Delta R')
        plt.legend()
        plt.show()
        '''
        x1s.append(c1[0])
        y1s.append(c1[1])
        r1s.append(r1)

        x2s.append(c2[0])
        y2s.append(c2[1])
        r2s.append(r2)
        '''


    def alignImages(self, rows: lite.Row):
        self.setReferences(rows)

        ia = ImageAlignment(self.retRef)
        ia.initiateSRReference()

        xs = []
        ys = []
        rs = []
        an = []

        with open('Test.csv', 'w') as file:
            for row in rows:
                ia.readImage(row['retinas'])
                ia.setRegistration()
                ia.readImage(row['rosas'])
                img = ia.transform()

                #cv2.imwrite('/testStack/{}'.format(os.path.basename(row['rosas'])), newImg)
                center, radius = self.findLaserSpot(img)

                xDiff = self.rosaRefPos[0] - center[0]
                yDiff = self.rosaRefPos[1] - center[1]

                xs.append(center[0])
                ys.append(center[1])
                rs.append(radius)
                an.append(os.path.basename(row['rosas'])[:-4])

                positionStr = "Ref Pos : {}, Center : {}, Delta : ({}, {})".format(self.rosaRefPos, center, xDiff, yDiff)
                radiusStr = "Ref Radius : {}, Radius : {}, Delta : {}".format(self.rosaRefRadius, radius, self.rosaRefRadius - radius)

                file.write("{}, {}\n".format(positionStr, radiusStr))

        plt.imshow(self.retRef[:, :, ::-1])
        plt.scatter(x=xs, y=ys, s=radius, linestyle='-', facecolors='none', edgecolors='w')
        for n, note in enumerate(an):
            plt.annotate(note, (xs[n], ys[n]), fontsize=8, color='w')
        plt.savefig('test.jpg')
        plt.show()


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
