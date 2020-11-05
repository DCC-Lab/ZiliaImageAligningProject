from ziliaImage.ImageAlignment import ImageAlignment
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ziliaImage.rosa.find_rosa_dc_v2 as ziv2
import ziliaImage.rosa.find_rosa_dc as ziv1
import os
import numpy as np
import cv2
import sqlite3 as lite


class ImageAnalysis:
    def __init__(self):
        self.retRef = None
        self.rosaRef = None
        self.rosaRefPos = None
        self.rosaRefRadius = None
        self.shapeRef = None
        #self.dictImages = self.SortImages(os.path.normpath("C:\\zilia"))
        #self.directories = self.dictImages.keys()

    def setReferences(self, rows: lite.Row):
        # For now, the reference doesn't really need to be any specific image.
        # I skip the first couple of images and ignore the first couple of remaining images.
        i = np.random.randint((len(rows) // 10) * 5, (len(rows) // 10) * 6)
        print(rows[i]['retinas'], rows[i]['rosas'])
        self.retRef = cv2.imread(rows[i]['retinas'], cv2.COLOR_BGR2GRAY)
        self.rosaRef = cv2.imread(rows[i]['rosas'], cv2.COLOR_BGR2GRAY)
        self.shapeRef = self.retRef.shape
        self.rosaRefPos, self.rosaRefRadiusm, found = self.findLaserSpot(self.rosaRef, 2)

    def findLaserSpot(self, img: np.ndarray, version: int):
        # FIXME Versions should be removed after testing is done!
        if version == 1:
            blob = ziv1.find_laser_spot_main_call(img)
        elif version == 2:
            blob, recTime, found = ziv2.find_laser_spot_main_call(img)
        else:
            raise ValueError('Version value should be 1 or 2, got {} instead!'.format(version))

        if self.shapeRef:
            center = (int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0]))
            radius = int(blob['radius'] * self.shapeRef[0])
        else:
            shape = img.shape
            center = (int(blob['center']['x'] * shape[1]), int(blob['center']['y'] * shape[0]))
            radius = int(blob['radius'] * shape[0])

        return center, radius, center != (0, 0)

    def compareVersionsOneImage(self, img: np.ndarray, iter=100):
        x1s, y1s, r1s, x2s, y2s, r2s = [], [], [], [], [], []

        for i in range(iter):
            c1, r1, found = self.findLaserSpot(img, 1)
            c2, r2, found = self.findLaserSpot(img, 2)

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

    def compareVersionsMultipleImages(self, rows: lite.Row):
        x1s, y1s, r1s, x2s, y2s, r2s = [], [], [], [], [], []
        dxs, dys, drs, axes = [], [], [], []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.findLaserSpot(img, 1)
            c2, r2, found = self.findLaserSpot(img, 2)

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
        plt.ylabel('Position [px]')
        plt.legend()

        plt.subplot(312)
        plt.plot(axes, y1s, 'r', label='Y V1')
        plt.plot(axes, y2s, 'b', label='Y V2')
        plt.plot(axes, dys, 'g--', label='Delta Y')
        plt.ylabel('Position [px]')
        plt.legend()

        plt.subplot(313)
        plt.plot(axes, r1s, 'r', label='R V1')
        plt.plot(axes, r2s, 'b', label='R V2')
        plt.plot(axes, drs, 'g--', label='Delta R')
        plt.ylabel('Rayon [px]')
        plt.xlabel("Num. de l'image")
        plt.legend()
        plt.show()

    def compareVersionsHistogram2D(self, rows: lite.Row, noZeroes=False):
        x1s, y1s, x2s, y2s, = [], [], [], []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.findLaserSpot(img, 1)
            c2, r2, found = self.findLaserSpot(img, 2)
            if noZeroes:
                if c1[0] != 0 and c1[1] != 0:
                    x1s.append(c1[0])
                    y1s.append(c1[1])
                if c2[0] != 0 and c2[1] != 0:
                    x2s.append(c2[0])
                    y2s.append(c2[1])
            else:
                x1s.append(c1[0])
                y1s.append(c1[1])
                x2s.append(c2[0])
                y2s.append(c2[1])

        fig, axes = plt.subplots(1, 2)
        axes[0].hist2d(x1s, y1s, bins=50)
        axes[0].set_xlabel('V1 x Position [px]')
        axes[0].set_ylabel('y Position [px]')
        axes[1].hist2d(x2s, y2s, bins=50)
        axes[1].set_xlabel('V2')
        plt.show()

    def compareVersionsHistogram(self, rows: lite.Row):
        r1s, r2s = [], []
        axes = []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.findLaserSpot(img, 1)
            c2, r2, found = self.findLaserSpot(img, 2)

            r1s.append(np.sqrt(c1[0] ** 2 + c1[1] ** 2))
            r2s.append(np.sqrt(c2[0] ** 2 + c2[1] ** 2))
            axes.append(n)

        plt.figure()
        plt.hist(r1s, 50, label='R V1')
        plt.hist(r2s, 50, label='R V2')
        plt.ylabel('Count')
        plt.xlabel('Rayon [px]')
        plt.legend()
        plt.show()

    def compareVersion3DPlot(self, rows: lite.Row):
        r1s, r2s = [], []

        xMesh, yMesh = np.meshgrid(np.arange(0, self.shapeRef[1], self.shapeRef[1]), np.arange(0, self.shapeRef[0], self.shapeRef[0]))
        z1s = np.zeros((self.shapeRef[0], self.shapeRef[1], 1))
        z2s = np.zeros((self.shapeRef[0], self.shapeRef[1], 1))

        for row in rows:
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.findLaserSpot(img, 1)
            c2, r2, found = self.findLaserSpot(img, 2)

            z1s[c1[1], c1[0], 0] += 1
            z2s[c2[1], c2[0], 0] += 1
            #r1s.append(np.sqrt(c1[0] ** 2 + c1[1] ** 2))
            #r2s.append(np.sqrt(c2[0] ** 2 + c2[1] ** 2))

        plt.figure()
        plt.gca(projection='3d')
        plt.show()

    def alignImages(self, rows: lite.Row):
        self.setReferences(rows)

        ia = ImageAlignment(self.retRef)
        ia.initiateSRReference()

        xs = []
        ys = []
        rs = []
        an = []

        with open('../tests/Test.csv', 'w') as file:
            for row in rows:
                ia.readImage(row['retinas'])
                ia.setRegistration()
                ia.readImage(row['rosas'])
                img = ia.transform()

                #cv2.imwrite('/testStack/{}'.format(os.path.basename(row['rosas'])), newImg)
                center, radius, found = self.findLaserSpot(img, 2)

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
