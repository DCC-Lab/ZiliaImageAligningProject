from .imageanalysis import ImageAnalysis
from ziliaImage.imagealignment import ImageAlignment
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ziliaImage.rosa.find_rosa_dc_v2 as ziv2
import ziliaImage.rosa.find_rosa_dc as ziv1
import os
import numpy as np
import cv2
import sqlite3 as lite
import logging
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from multiprocessing import Pool


class ImageAnalytics(ImageAnalysis):
    # This is a version of ImageAnalysis that is meant for testing and graphs.
    # For the purpose of aligning images and getting the laser spots, ImageAnalysis is much better suited.
    def __init__(self, rows: lite.Row):
        super().__init__(rows)

    def laserSpot(self, img: np.ndarray, version: int = 2):
        # FIXME Versions should be removed after testing is done!
        if version == 1:
            blob = ziv1.find_laser_spot_main_call(img)
        elif version == 2:
            blob, recTime, found = ziv2.find_laser_spot_main_call(img)
        else:
            raise ValueError('Version value should be 1 or 2, got {} instead!'.format(version))

        if self.shapeRef:
            center = [int(blob['center']['x'] * self.shapeRef[1]), int(blob['center']['y'] * self.shapeRef[0])]
            radius = int(blob['radius'] * self.shapeRef[0])
        else:
            shape = img.shape
            center = (int(blob['center']['x'] * shape[1]), int(blob['center']['y'] * shape[0]))
            radius = int(blob['radius'] * shape[0])

        return center, radius, center != (0, 0)

    # FIXME I don't think this is useful...
    def laserSpots(self, rows: lite.Row):
        cs, rs, fs = [], [], []

        for row in rows:
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            center, radius, found = self.laserSpot(img)
            cs.append(center)
            rs.append(radius)
            fs.append(found)

        return cs, rs, fs

    def prepareForPickling(self, rows: lite.Row):
        # We're not talking about actual pickles!
        for row in rows:
            yield [row['retinas'], row['rosas']]

    def compareVersionsOneImage(self, img: np.ndarray, iter=100):
        x1s, y1s, r1s, x2s, y2s, r2s = [], [], [], [], [], []

        for i in range(iter):
            c1, r1, found = self.laserSpot(img, 1)
            c2, r2, found = self.laserSpot(img, 2)

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

            c1, r1, found = self.laserSpot(img, 1)
            c2, r2, found = self.laserSpot(img, 2)

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
        #plt.plot(axes, dxs, 'g--', label='Delta X')
        plt.ylabel('Position [px]')
        plt.legend()

        plt.subplot(312)
        plt.plot(axes, y1s, 'r', label='Y V1')
        plt.plot(axes, y2s, 'b', label='Y V2')
        #plt.plot(axes, dys, 'g--', label='Delta Y')
        plt.ylabel('Position [px]')
        plt.legend()

        plt.subplot(313)
        plt.plot(axes, r1s, 'r', label='R V1')
        plt.plot(axes, r2s, 'b', label='R V2')
        #plt.plot(axes, drs, 'g--', label='Delta R')
        plt.ylabel('Rayon [px]')
        plt.xlabel("Num. de l'image")
        plt.legend()
        plt.show()

    # This is not suited for our purpose at all.
    def compareVersionsHistogram2D(self, rows: lite.Row, noZeroes=False):
        x1s, y1s, x2s, y2s, = [], [], [], []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.laserSpot(img, 1)
            c2, r2, found = self.laserSpot(img, 2)
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

    '''
    # FIXME This was generally a bad idea. It also doesn't work.
    def compareVersion3DPlot(self, rows: lite.Row):
        r1s, r2s = [], []

        xMesh, yMesh = np.meshgrid(np.arange(0, self.shapeRef[1], self.shapeRef[1]), np.arange(0, self.shapeRef[0], self.shapeRef[0]))
        z1s = np.zeros((self.shapeRef[0], self.shapeRef[1]))
        z2s = np.zeros((self.shapeRef[0], self.shapeRef[1]))

        for row in rows:
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.laserSpot(img, 1)
            c2, r2, found = self.laserSpot(img, 2)

            z1s[c1[1], c1[0]] += 1
            z2s[c2[1], c2[0]] += 1
            #r1s.append(np.sqrt(c1[0] ** 2 + c1[1] ** 2))
            #r2s.append(np.sqrt(c2[0] ** 2 + c2[1] ** 2))

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X=xMesh, Y=yMesh, Z=z1s)
        fig.colorbar(surf)
        plt.show()
    '''

    def compareVersionsHistogram(self, rows: lite.Row):
        r1s, r2s = [], []
        axes = []

        for n, row in enumerate(rows):
            img = cv2.imread(row['rosas'], cv2.COLOR_BGR2GRAY)

            c1, r1, found = self.laserSpot(img, 1)
            c2, r2, found = self.laserSpot(img, 2)

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

    def testBadDetectionV2(self, rows: lite.Row = None):
        if rows is not None:
            self.setReferences(rows)

        xs, ys, rs = [], [], []
        txs, tys, trs = [], [], []
        wxs, wys, wrs = [], [], []

        '''
        images = self.prepareForPickling(rows)

        with Pool() as p:
            # Multiprocess read
            retina, rosa = p.map(self.ia.readImagePair, images)
            p.map(self.ia.imgToRegister, retina)
            p.mao(self.ia.imgToTransform, rosa)

            # Multiprocess laser spots on unaltered image.
            center, radius, found = p.map(self.laserSpot, self.ia.rosa)
            p.map(xs.append, center[0])
            p.map(ys.append, center[1])
            p.map(rs.append, radius)

            # Multiprocess transform on rosas.
            trosa = p.apply_async(self.ia.registerAndTransform)

            # Multiprocess laser spots on transformed images.
            tcenter, tradius, tfound = p.map(self.laserSpot, trosa)
            p.map(txs.append, tcenter[0])
            p.map(tys.append, tcenter[1])
            p.map(trs.append, tradius)

            if abs(center[0] - tcenter[0]) > 150 or abs(center[1] - tcenter[1]) > 150:
                p.map(wxs.append, tcenter[0])
                p.map(wys.append, tcenter[1])
                p.map(wrs.append, tradius)

        '''
        newRows = self.prepareForPickling(self.rows)

        for row in newRows:
            self.ia.imgToRegister(row[0])
            self.ia.setRegistration()
            self.ia.imgToTransform(row[1])
            img = self.ia.traImg
            newImg = self.ia.transform()
            print(img, newImg)

            with Pool() as p:
                center, radius, found = p.map(self.laserSpot, [img, newImg])

            print(center, radius, found)

            center, radius, found = self.laserSpot(self.ia.traImg, 2)
            xs.append(center[0])
            ys.append(center[1])
            rs.append(radius)

            tcenter, tradius, tfound = self.laserSpot(newImg, 2)
            txs.append(tcenter[0] + self.shapeRef[1])
            tys.append(tcenter[1])
            trs.append(tradius)

            if self.checkDisplacement(center, tcenter):
                wxs.append(tcenter[0] + self.shapeRef[1])
                wys.append(tcenter[1])
                wrs.append(tradius)

        # FIXME This should be removed
        txs = txs + self.shapeRef[1]
        wxs = wxs + self.shapeRef[1]

        image = np.zeros((self.shapeRef[0], self.shapeRef[1] * 2, self.shapeRef[2]), dtype=np.int32)
        image[:, 0:2448, :] = self.retRef[:, :, ::-1]
        image[:, 2448:4896, :] = self.retRef[:, :, ::-1]

        plt.figure()
        plt.imshow(image)
        plt.scatter(xs, ys, s=rs, facecolors='none', edgecolors='white')
        plt.scatter(txs, tys, s=trs, facecolors='none', edgecolors='white')
        plt.scatter(wxs, wys, s=wrs, c='r', marker='+')
        plt.show()

    def testClusteringV2(self, rows: lite.Row):
        self.setReferences(rows)

        ia = ImageAlignment(self.retRef)
        ia.initiateSRReference()

        points = np.zeros((len(rows), 2))
        sizes = []

        for n, row in enumerate(rows):
            #ia.imgToTransform(row['retinas'])
            #ia.setRegistration()
            ia.imgToTransform(row['rosas'])
            #img = ia.transform()
            img = ia.traImg
            center, radius, found = self.laserSpot(img, 2)
            if found:
                points[n, :] = [center[0], center[1]]
                sizes.append(radius)

        yhc = self.agglomerativeClustering(points)

        plt.figure()
        plt.imshow(self.retRef[:, :, ::-1])
        colors = ['#000000', '#555555', '#999999', '#bbbbbb', '#ffffff', '#550000', '#990000', '#bb0000', '#ff0000',
                  '#005500', '#009900', '#00bb00', '#00ff00', '#000055', '#000099', '#0000bb', '#0000ff', '#555500',
                  '#999900', '#bbbb00', '#ffff00', '#005555', '#009999', '#00bbbb', '#00ffff', '#550055', '#990099',
                  '#bb00bb', '#ff00ff']
        for i in range(len(colors)):
            plt.scatter(points[yhc == i, 0], points[yhc == i, 1], s=sizes, facecolors='none', edgecolors=colors[i])
        plt.show()

    def agglomerativeClustering(self, points: np.ndarray):
        # create clusters
        hc = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='single', distance_threshold=100)
        # save clusters for chart
        yhc = hc.fit_predict(points)
        return yhc

    def alignImagesV1(self, rows: lite.Row):
        self.setReferences(rows)

        ia = ImageAlignment(self.retRef)
        ia.initiateSRReference()

        xs, ys, rs, an = [], [], [], []

        with open('../tests/Test.csv', 'w') as file:
            for row in rows:
                ia.imgToTransform(row['retinas'])
                ia.setRegistration()
                ia.imgToTransform(row['rosas'])
                img = ia.transform()
                center, radius, found = self.laserSpot(img, 2)

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