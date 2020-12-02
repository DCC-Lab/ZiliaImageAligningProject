from ziliaImage.imagealignment import ImageAlignment
import ziliaImage.rosa.find_rosa_dc_v2 as ziv2
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as lite
import tifffile as tiff
import os
import cv2


class ImageAnalysis:
    def __init__(self, rows: lite.Row):
        self.rows = rows
        self.retRef = None
        self.rosaRef = None
        self.rosaRefPos = None
        self.rosaRefRadius = None
        self.shapeRef = None
        self.ia = None
        self.setReferences(rows)

    def setReferences(self, rows: lite.Row):
        self.rows = rows
        # For now, the reference doesn't really need to be any specific image.
        # I skip the first couple of images and ignore the first couple of remaining images.
        i = np.random.randint((len(rows) // 10) * 5, (len(rows) // 10) * 6)
        print(rows[i]['retinas'], rows[i]['rosas'])
        self.retRef = cv2.imread(rows[i]['retinas'], cv2.COLOR_BGR2GRAY)
        self.rosaRef = cv2.imread(rows[i]['rosas'], cv2.COLOR_BGR2GRAY)
        self.shapeRef = self.retRef.shape

        self.ia = ImageAlignment(self.retRef)
        self.ia.initiateSRReference()

    def laserSpot(self, img: np.ndarray):
        blob, recTime, found = ziv2.find_laser_spot_main_call(img)

        if self.shapeRef:
            center = [int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0])]
            radius = int(blob['radius'] * self.shapeRef[0])
        else:
            shape = img.shape
            center = (int(blob['center']['x'] * shape[1]), int(blob['center']['y'] * shape[0]))
            radius = int(blob['radius'] * shape[0])

        return center, radius, center != (0, 0)

    def stdDisplacement(self, centers, tcenters):
        xDis = []
        yDis = []
        # Removing zeros
        for n, center in enumerate(centers):
            if center[0] > 100 and center[1] > 100 and tcenters[n, 0] > 100 and tcenters[n, 1] > 100:
                xDis.append(tcenters[n, 0] - center[0])
                yDis.append(tcenters[n, 1] - center[1])

        # X and Y STD with the number of sigmas we want :
        xStd = np.std(xDis)
        yStd = np.std(yDis)
        factor = 3
        print('Standard Deviations is {} in x and is {} in y. Factor is {}.'.format(xStd, yStd, factor))

        wPtsIndex = []
        for n in range(len(xDis)):
            if np.abs(xDis[n]) > factor * xStd or np.abs(yDis[n]) > factor * yStd:
                wPtsIndex.append(n)

        wrongPoints = np.zeros((len(wPtsIndex), 3))
        for n, ind in enumerate(wPtsIndex):
            wrongPoints[n, :] = tcenters[ind]

        return wrongPoints

    def checkDisplacement(self, center1, center2, threshold=150):
        if abs(center1[0] - center2[0]) > threshold or abs(center1[1] - center2[1]) > threshold:
            return False
        else:
            return True

    def alignImages(self, rows: lite.Row = None, makeGraph=False, makeStack=False):
        if rows is not None:
            self.setReferences(rows)

        txs, tys, trs = [], [], []

        centers = np.zeros((len(self.rows), 3))
        tcenters = np.copy(centers)

        '''
        if makeStack:
            stack = np.zeros((len(self.rows), self.shapeRef[0], self.shapeRef[1], self.shapeRef[2]))
        '''

        for n, row in enumerate(self.rows):
            self.ia.imgToRegister(row['retinas'])
            self.ia.setRegistration()

            self.ia.imgToTransform(row['rosas'])
            img = self.ia.traImg
            newImg = self.ia.transform()

            center, radius, found = self.laserSpot(img)
            centers[n, :] = [center[0], center[1], radius]

            tcenter, tradius, tfound = self.laserSpot(newImg)
            tcenters[n, :] = [tcenter[0], tcenter[1], tradius]

            txs.append(tcenter[0])
            tys.append(tcenter[1])
            trs.append(tradius)

            '''
            if makeStack:
                stack[n, :, :, :] = newImg[:, :, ::-1]
            '''

        wrongPoints = self.stdDisplacement(centers, tcenters)
        image = np.zeros(self.shapeRef, dtype=np.int32)
        image[:, :, :] = self.retRef[:, :, ::-1]

        plt.figure()
        plt.imshow(image)
        plt.scatter(txs, tys, s=trs, facecolors='none', edgecolors='white')
        plt.scatter(wrongPoints[:, 0], wrongPoints[:, 1], s=wrongPoints[:, 2], c='r', marker='+')
        plt.imsave(os.path.join(os.path.dirname(self.retRef), 'test.jpg'))
        plt.show()

        '''
        if makeGraph:
            image = np.zeros(self.shapeRef, dtype=np.int32)
            image[:, :, :] = self.retRef[:, :, ::-1]

            plt.figure()
            plt.imshow(image)
            plt.scatter(txs, tys, s=trs, facecolors='none', edgecolors='white')
            plt.scatter(wrongPoints[:, 0], wrongPoints[:, 1], s=wrongPoints[:, 2], c='r', marker='+')
            plt.imsave(os.path.basename(rows['retinas']))
            plt.show()

            plt.figure()
            plt.hist(np.abs(tcenters[:, :1] - centers[:, :1]), 50, label='X')
            plt.ylabel('Count [-]')
            plt.xlabel('Displacement [px]')
            plt.legend()
            plt.show()

            plt.figure()
            plt.hist(np.abs(tcenters[:, 1:2] - centers[:, 1:2]), 50, label='Y')
            plt.ylabel('Count [-]')
            plt.xlabel('Displacement [px]')
            plt.legend()
            plt.show()

        if makeStack:
            tiff.imwrite(os.path.join(os.getcwd(), 'tempfiles', 'stack.tiff'), stack)
        '''

        return txs, tys, trs
