import sqlite3 as lite
import os
import fnmatch
import re
import cv2
from database.database import Database
from utilities import findFiles
import numpy as np
import time


class ZiliaDatabase(Database):
    def __init__(self, pathToDB=None):
        if pathToDB is None:
            path = self.defaultPath()
        else:
            path = pathToDB

        super().__init__(path)

    def defaultPath(self):
        return 'zilia.db'

    def getJpgs(self, root: str, files: list) -> list:
        jpgs = []
        for file in files:
                if fnmatch.fnmatch(file, "*.jpg"):
                    jpgs.append(os.path.join(root, file))
        return jpgs

    def getCSV(self, root: str, files: list) -> str:
        csv = "None"
        for file in files:
            if fnmatch.fnmatch(file, "*.csv"):
                csv = os.path.join(root, file)
        return csv

    def getMonkey(self, root: str) -> str:
        try:
            associatedMonkey = re.findall('sing*e[0-9][0-9]|sing*e[0-9]', root)[0]
        except:
            associatedMonkey = "None"

        return associatedMonkey

    def getSeries(self, root):
        for rt, directories, files in os.walk(os.path.normpath(root)):
            # We check if there are jpgs in the current directory.
            jpgs = self.getJpgs(rt, files)

            # If there are JPGs, we proceed.
            if jpgs:
                totImages = len(jpgs)
                spectrasPath = self.getCSV(rt, files)
                associatedMonkey = self.getMonkey(rt)
                seriesName = os.path.basename(rt)
                seriesPath = os.path.normpath(rt)

                serie = {"name": seriesName, "monkey": associatedMonkey, "images": totImages, "spectra": spectrasPath,
                         "path": seriesPath}
                yield serie

    def sortRetinasAndRosas(self, imagePaths: list):
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
        return retinas, rosas

    def setupMainSeriesTable(self, data: list):
        if self.isConnected:
            statement = 'CREATE TABLE IF NOT EXISTS "series" (name TEXT, monkey TEXT, images INT, spectra TEXT, ' \
                        'path TEXT)'
            self.execute(statement)

            for entry in data:
                fields = []
                items = []
                for field, item in entry.items():
                    fields.append('"{}"'.format(str(field)))
                    items.append('"{}"'.format(str(item)))
                statement = 'INSERT OR REPLACE INTO "series" ({}) VALUES ({})'.format(', '.join(fields), ', '.join(items))
                self.execute(statement)

    def setupImageTable(self, rows: lite.Row):
        if self.isConnected:
            # Create the table for the serie :
            statement = 'CREATE TABLE IF NOT EXISTS "images" (serie TEXT, monkey TEXT, retinas TEXT PRIMARY KEY, rosas TEXT)'
            self.execute(statement)

            for row in rows:
                jpgs = findFiles(row['path'], '*.jpg')
                retinas, rosas = self.sortRetinasAndRosas(jpgs)
                n = 0
                print("Inserting serie {}".format(row['name']))
                for rosa in rosas:
                    try:
                        statement = 'INSERT OR REPLACE INTO "images" ({}) VALUES ("{}", "{}", "{}", "{}")'\
                            .format('"serie", "monkey", "retinas", "rosas"', row["name"], row["monkey"], retinas[n], rosa)
                        self.execute(statement)
                    except:
                        print("An insertion failed for the serie {}!".format(row['name']))
                    n += 1

    @staticmethod
    def createZiliaDB(path: str):
        # Proceeding to creating the database...
        with ZiliaDatabase(path) as db:
            print('Changing to rwc mode...')
            db.changeConnectionMode('rwc')

            tables = db.tables
            if tables:
                print('Dropping old tables...')
                for table in tables:
                    db.dropTable(table)
                print('Done!')
            else:
                print('There are no tables, proceeding...')

            print('Putting Database in asynchronous mode... Only one person should proceed at once...')
            db.asynchronous()

            # Setting up the main table containing all of the series and some general information.
            print("Setting up the main series Table.")
            series = db.getSeries("C:\\zilia")
            db.beginTransaction()
            db.setupMainSeriesTable(series)
            db.endTransaction()
            print("Done...")

    @staticmethod
    def createImagesTable(path: str):
        with ZiliaDatabase(path) as db:
            print('Changing to rwc mode...')
            db.changeConnectionMode('rwc')

            print('Putting Database in asynchronous mode... Only one person should proceed at once...')
            db.asynchronous()

            print("Dropping the images table...")
            db.dropTable("images")

            # Now, we can grab all of the series and their path :
            print("Querrying all series...")
            rows = db.select('series', 'name, monkey, path')

            print("Setting up images table...")
            db.setupImageTable(rows)

            print('Done...')
