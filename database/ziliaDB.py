from database.database import Database
from utilities import findFiles
from ziliaImage.rosa.find_rosa_dc_v2 import find_laser_spot_main_call
import sqlite3 as lite
import numpy as np
import os
import fnmatch
import re
import cv2
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
            associatedMonkey = str(re.findall('sing*e[0-9][0-9]|sing*e[0-9]', root, re.IGNORECASE)[0]).lower()
        except:
            associatedMonkey = "None"

        return associatedMonkey

    def getSeriesType(self, root: str) -> str:
        try:
            seriesType = str(re.findall('darkref', root, re.IGNORECASE)[0]).lower()
        except:
            seriesType = "normal"

        return seriesType

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
                seriesType = self.getSeriesType(rt)

                serie = {"name": seriesName, "monkey": associatedMonkey, "images": totImages, "spectra": spectrasPath,
                         "path": seriesPath, "type": seriesType, "problems": 'None'}
                yield serie

    def readSpectra(self, csvPath: str):
        #FIXME Header is sometime 2 lines, sometime 3 lines. Great.
        # Wavelength is a list, Lines is a list of lists containing the intensities.
        with open(csvPath, 'r') as f:
            spectra = f.readlines()
            spectra.pop(0)

            # Separate the wavelengths from the values.
            wavelengths = spectra.pop(0).replace('\n', '').split(',')
            try:
                float(wavelengths[0])
            except:
                wavelengths = spectra.pop(0).replace('\n', '').split(',')

        for n, spectrum in enumerate(spectra):
            spectra[n] = spectrum.replace('\n', '').split(',')

        return wavelengths, spectra

    def ignoreFolder(self, path):
        boo = False
        #if re.findall('jour 1', path, re.IGNORECASE) or re.findall('darkref', path, re.IGNORECASE):
        if re.findall('darkref', path, re.IGNORECASE):
            boo = True
        return boo

    def setupMainSeriesTable(self, data: list):
        if self.isConnected:
            statement = 'CREATE TABLE IF NOT EXISTS "series" (name TEXT, monkey TEXT, images INT, spectra TEXT, ' \
                        'path TEXT, type TEXT, problems TEXT)'
            self.execute(statement)

            for entry in data:
                fields = []
                items = []
                for field, item in entry.items():
                    fields.append('"{}"'.format(str(field)))
                    items.append('"{}"'.format(str(item)))
                statement = 'INSERT OR REPLACE INTO "series" ({}) VALUES ({})'.format(', '.join(fields), ', '.join(items))
                self.execute(statement)

    def setupImagesTable(self, rows: lite.Row):
        if self.isConnected:
            # Create the table for the serie :
            statement = 'CREATE TABLE IF NOT EXISTS "images" (serie TEXT, monkey TEXT, images TEXT PRIMARY KEY, ' \
                        'bluemean INT, bluemin INT, greenmean INT, greenmin INT, redmean INT, redmin INT, ' \
                        'imagetype TEXT)'
            self.execute(statement)

            for row in rows:
                print('Computing serie {}...'. format(row['name']))
                jpgs = findFiles(row['path'], '*.jpg')
                print('{} images found for the serie. Assigning types to the images...'.format(len(jpgs)))
                images = self.imageTypes(jpgs)
                print('Insertion...')
                for image in images:
                    path, blueMean, blueMin, greenMean, greenMin, redMean, redMin, imType = image
                    values = '"{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"'.format(row['name'], row['monkey'], path, blueMean, blueMin, greenMean, greenMin, redMean, redMin, imType)
                    statement = 'INSERT OR REPLACE INTO "images" ("serie", "monkey", "images", "bluemean", ' \
                                '"bluemin", "greenmean", "greenmin", "redmean", "redmin", "imagetype") ' \
                                'VALUES ({})'.format(values)
                    self.beginTransaction()
                    self.execute(statement)
                    self.endTransaction()

    def imageTypes(self, imagePaths):
        images, redMeans, redMins = [], [], []

        for path in imagePaths:
            image = cv2.imread(path, cv2.COLOR_BGR2GRAY)

            # 0 for Blue, 1 for Green, 2 for Red :
            blueMean = np.mean(image[600:1800, 500:1500, 0])
            blueMin = np.min(image[600:1800, 500:1500, 0])
            greenMean = np.mean(image[600:1800, 500:1500, 1])
            greenMin = np.min(image[600:1800, 500:1500, 1])
            redMean = np.mean(image[600:1800, 500:1500, 2])
            redMin = np.min(image[800:1600, 660:1320, 2])

            redMeans.append(redMean)
            redMins.append(redMin)
            imType = ''

            images.append([path, blueMean, blueMin, greenMean, greenMin, redMean, redMin, imType])

        redMeans = np.mean(redMeans)
        redMins = np.mean(redMins)

        for n, image in enumerate(images):
            path, redMean, redMin, imType = image[0], image[5], image[6], image[7]
            if redMean > redMeans and redMin > redMins:
                imType = 'retina'
            elif redMean < redMeans and redMin < redMins:
                imType = 'rosa'
            else:
                imType = 'error'
            images[n][7] = imType

        return images

    # FIXME To be removed.
    '''
    def setupImageTable(self, rows: lite.Row):
        if self.isConnected:
            # Create the table for the serie :
            statement = 'CREATE TABLE IF NOT EXISTS "images" (serie TEXT, monkey TEXT, retinas TEXT PRIMARY KEY, ' \
                        'rosas TEXT, position TEXT, spectra TEXT)'
            self.execute(statement)

            for row in rows:
                print('Computing serie {}...'. format(row['name']))

                if self.ignoreFolder(row['path']) is False:
                    # Get the spectra for the associated series :
                    if row['spectra'] != 'None':
                        wavelengths, spectra = self.readSpectra(row['spectra'])
                        print('Serie has {} spectra.'.format(len(spectra)))

                        # Rearranging the wavelengths and spectra together
                        spec = []
                        for spectrum in spectra:
                            spec.append([wavelengths, spectrum])
                    else:
                        print('Serie has no spectra!')

                    # Sorting the retinas and ROSAs...
                    print('Sorting the images...')
                    jpgs = findFiles(row['path'], '*.jpg')
                    retinas, rosas, validated = self.sortRetinasAndRosas(jpgs)
                    print('Serie has {} retinas and {} ROSAs.'.format(len(retinas), len(rosas)))

                    print("Insertion...")
                    for n, rosa in enumerate(rosas):
                        try:
                            statement = 'INSERT OR REPLACE INTO "images" ({}) VALUES ("{}", "{}", "{}", "{}")'\
                                .format('"serie", "monkey", "retinas", "rosas"', row["name"], row["monkey"], retinas[n],
                                        rosa)
                            self.execute(statement)
                        except IndexError:
                            print("An insertion failed for the serie {}! Index out of range {}".format(row['name'], n))
                else:
                    print('{} is not a valid data serie. It will be ignored.'.format(row['name']))

                # We want to check if the images were validated. If they were not validated, we want to flag the series as problematic.
    '''

    def setupTripletsTable(self, rows: lite.Row):
        if self.isConnected:
            statement = 'CREATE TABLE IF NOT EXISTS "triplets" (serie TEXT, monkey TEXT, retinas TEXT PRIMARY KEY, ' \
                        'rosas TEXT, x INT, y INT, deltax INT, deltay INT, radius INT, spectra TEXT)'
            self.execute(statement)

            retinas, rosas, erroneous = self.sortImagesByType(rows)
            pass

    def sortImagesByType(self, rows: lite.Row):
        imagesTypes = []
        for row in rows:
            imagesTypes.append(row['imagetype'])

        retinas = []
        rosas = []
        erroneous = []

        for n, row in enumerate(rows):
            imType = row['imagetype']
            if imType == 'retina':
                if 0 < n < (len(rows) - 1):
                    # if the retina is flanked by rosa, it's most likely a retina.
                    if imagesTypes[n - 1] == 'rosa' and imagesTypes[n + 1] == 'rosa':
                        retinas.append(row)
                    # If the retina is flanked by retinas, it's probably a wrong retina flag and must be a rosa.
                    elif imagesTypes[n - 1] == 'retina' and imagesTypes[n - 1] == 'retina':
                        erroneous.append(row)
                        imagesTypes[n] = 'rosa'
                        rosas.append(row)
                    # If the retina is flanked by a retina and a rosa, we need to check if the previous rosa and the
                    # next rosa are similar.
                    # In such a case, we can copy one of them as the rosa for the current retina.
                    elif imagesTypes[n - 1] == 'retina' and imagesTypes[n + 1] == 'rosa':
                        if imagesTypes[n - 2] == 'rosa':
                            prevRosa = cv2.imread(rows[n - 2]['images'], cv2.COLOR_BGR2GRAY)
                            nextRosa = cv2.imread(rows[n + 1]['images'], cv2.COLOR_BGR2GRAY)

                            pCenter, pRadius, found = find_laser_spot_main_call(prevRosa)
                            nCenter, nRadius, found = find_laser_spot_main_call(nextRosa)
                            # If the difference between the two rosas is within 1%, we can copy it.
                            if ((pCenter[0] - nCenter[0]) / nCenter[0]) * 100 < 1 and ((pCenter[1] - nCenter[1]) /
                                                                                       nCenter[1]) * 100 < 1:
                                retinas.append(row)
                                rosas.append(rows[n - 2])
                            else:
                                retinas.append(row)
                                rosas.append('None')
                    else:
                        retinas.append(row)

            elif imType == 'rosa':
                if 0 < n < (len(rows) - 1):
                    # if the retina is flanked by rosa, it's most likely a retina.
                    if imagesTypes[n - 1] == 'rosa' and imagesTypes[n + 1] == 'rosa':
                        erroneous.append(row)
                        imagesTypes[n] = 'retina'
                        retinas.append(row)
                    # If the retina is flanked by retinas, it's probably a wrong retina flag and must be a rosa.
                    elif imagesTypes[n - 1] == 'retina' and imagesTypes[n - 1] == 'retina':
                        rosas.append(row)

                    # If the retina is flanked by a rosa and a retina, we are missing a retina and can't really do
                    # anything about it.
                    elif imagesTypes[n - 1] == 'rosa' and imagesTypes[n + 1] == 'retina':
                        retinas.append('None')
                        rosas.append(row)
                    else:
                        rosas.append(row)
                else:
                    rosas.append(row)

            elif imType == 'error':
                if 0 < n < (len(rows) - 1):
                    # If the image is flanked by rosas, it should be a retina.
                    if imagesTypes[n - 1] == 'rosa':
                        imagesTypes[n] = 'retina'
                        retinas.append(row)
                    # If the image is flanked by retinas, it should be a rosa.
                    elif imagesTypes[n - 1] == 'retina':
                        imagesTypes[n] = 'rosa'
                        rosas.append(row)

            else:
                raise TypeError('Image is not a recognized type. Type is : {}'.format(imType))

        print('Retinas = {}, ROSAs = {}, Erroneous = {}'.format(len(retinas), len(rosas), len(erroneous)))
        return retinas, rosas, erroneous

    @staticmethod
    def createZiliaDB(dbPath: str, imgPath: str):
        # Proceeding to creating the database...
        with ZiliaDatabase(dbPath) as db:
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

            print('Putting Database in asynchronous mode. Only one person should proceed at once.')
            db.asynchronous()

            # Setting up the main table containing all of the series and some general information.
            print("Setting up the main series Table.")
            series = db.getSeries(imgPath)
            db.setupMainSeriesTable(series)
            print("Done!")
        print("...Exit.")

    @staticmethod
    def createImagesTable(dbPath: str):
        with ZiliaDatabase(dbPath) as db:
            print('Changing to rwc mode...')
            db.changeConnectionMode('rwc')

            print('Putting Database in asynchronous mode... Only one person should proceed at once...')
            db.asynchronous()

            print("Dropping the images table...")
            db.dropTable("images")

            # Now, we can grab all of the series and their path :
            print("Querrying all series...")
            rows = db.select('series')

            print("Setting up images table...")
            db.setupImagesTable(rows)

            print('Done!')
        print("...Exit.")

    @staticmethod
    def createTripletsTable(dbPath: str):
        with ZiliaDatabase(dbPath) as db:
            print('Changing to rwc mode...')
            db.changeConnectionMode('rwc')

            print('Putting Database in asynchronous mode... Only one person should proceed at once...')
            db.asynchronous()

            print("Dropping the triplets table...")
            db.dropTable("triplets")

            print("Querrying all series...")
            series = db.select('series')
            for serie in series:
                images = db.select('images', condition='"serie" IS "{}" ORDER BY "images" ASC'.format(serie['name']))
                db.setupTripletsTable(images)

            # We need to querry all the series. Then, serie by serie, we get the images. Then, image by image, we create the triplets.

# FIXME To be removed.
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