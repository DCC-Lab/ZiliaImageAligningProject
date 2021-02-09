from database.database import Database
from utilities import findFiles
from ziliaImage.rosa.find_rosa_dc_v2 import find_laser_spot_main_call
from xlsx.ziliaxlsx import ZiliaXLSX
import sqlite3 as lite
import numpy as np
import os
import fnmatch
import re
import cv2


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
            # RE is made following these rules : Sometimes we have singge##,
            # sometimes we have sing##,
            # sometimes we have singe##,
            associatedMonkey = str(re.findall('sing+e?([0-9]+)', root, re.IGNORECASE)[0])
        except:
            associatedMonkey = "None"

        return associatedMonkey

    def getSeriesType(self, root: str) -> str:
        try:
            seriesType = str(re.findall('darkref|pureonh', root, re.IGNORECASE)[0]).lower()
        except:
            seriesType = "normal"

        return seriesType

    # FIXME For later, once we know what the variables are.
    def getAcquisitionVariables(self, root: str) -> list:
        try:
            variables = str(re.findall('[0-9]*-[0-9]*-[0-9]*-[0-9]*', root, re.IGNORECASE)[0]).split('-')
        except:
            variables = ['0', '0', '0', '0']

        return variables

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
        with open(csvPath, 'r') as f:
            spectra = f.readlines()

            # We do this to remove the header and get the wavelengths. Since the header can be 2 lines at times and 3 at
            # others, we can't assume which line is which. We only assume that the first line of floats would be
            # wavelengths.
            for spectrum in spectra:
                try:
                    wavelengths = spectrum.replace('\n', '').split(',')
                    float(wavelengths[0])
                    break
                except:
                    spectra.pop(0)
                    pass

        intensities = []
        for n, spectrum in enumerate(spectra):
            intensities.append(spectrum.replace('\n', '').split(','))

        return wavelengths, intensities

    def setupMainSeriesTable(self, data: list):
        if self.isConnected:
            statement = 'CREATE TABLE IF NOT EXISTS "series" (serie_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                        'name TEXT SECONDARY KEY, monkey TEXT, images INT, spectra TEXT, path TEXT, type TEXT, ' \
                        'problems TEXT)'
            self.execute(statement)

            for entry in data:
                fields = []
                items = []
                for field, item in entry.items():
                    fields.append('"{}"'.format(str(field)))
                    items.append('"{}"'.format(str(item)))
                statement = 'INSERT OR REPLACE INTO "series" ({}) VALUES ({})'.format(', '.join(fields),
                                                                                      ', '.join(items))
                self.execute(statement)

    def setupMonkeysTable(self, keys: dict):
        if self.isConnected:
            fields = []
            for col in keys:
                fields.append('{} {}'.format(col, keys[col]))

            statement = 'CREATE TABLE IF NOT EXISTS "monkeys" ({})'.format(', '.join(fields))
            self.execute(statement)

    def setupImagesTable(self, rows: lite.Row):
        if self.isConnected:
            # Create the table for the serie :
            statement = 'CREATE TABLE IF NOT EXISTS "images" (image_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                        'serie TEXT, monkey TEXT, images TEXT SECONDARY KEY, bluemean INT, greenmean INT, ' \
                        'redmean INT, imagetype TEXT)'
            self.execute(statement)

            for row in rows:
                print('Computing serie {}...'. format(row['name']))
                if row['type'] == 'darkref':
                    print('Serie is a Dark Reference serie, passing...')
                elif row['type'] == 'pureonh':
                    print('Serie is a PUREONH serie, passing...')
                else:
                    jpgs = findFiles(row['path'], '*.jpg')
                    print('{} images found for the serie. Assigning types to the images...'.format(len(jpgs)))
                    images = self.sortImages(jpgs)
                    print('Insertion...')
                    self.beginTransaction()
                    for image in images:
                        path, blueMean, greenMean, redMean, imType = image
                        values = '"{}", "{}", "{}", "{}", "{}", "{}", "{}"'.format(row['name'], row['monkey'], path,
                                                                                   blueMean, greenMean, redMean, imType)
                        statement = 'INSERT OR REPLACE INTO "images" ("serie", "monkey", "images", "bluemean",' \
                                    ' "greenmean", "redmean", "imagetype") ' \
                                    'VALUES ({})'.format(values)
                        self.execute(statement)
                    self.endTransaction()

    def sortImages(self, imagePaths):
        imagePaths.sort(key=lambda imPath: int(re.sub('\D', '', imPath[-8:])))
        images, redMeans = [], []

        for path in imagePaths:
            image = cv2.imread(path, cv2.COLOR_BGR2GRAY)

            # 0 for Blue, 1 for Green, 2 for Red :
            blueMean = np.mean(image[600:1800, 500:1500, 0])
            greenMean = np.mean(image[600:1800, 500:1500, 1])
            redMean = np.mean(image[600:1800, 500:1500, 2])

            redMeans.append(redMean)
            imType = ''

            images.append([path, blueMean, greenMean, redMean, imType])

        redMeans = np.mean(redMeans)

        for n, image in enumerate(images):
            path, redMean, imType = image[0], image[3], image[4]
            if redMean > redMeans:
                imType = 'retina'
            elif redMean < redMeans:
                imType = 'rosa'
            else:
                imType = 'error'
            images[n][4] = imType

        sortedImages = self.validateSorting(images)

        return sortedImages

    def validateSorting(self, images: list) -> list:
        sortedImages = []

        for n, image in enumerate(images):
            imType = image[4]
            if 0 < n < (len(images) - 1):
                if imType == 'retina':
                    if images[n + 1][4] == 'rosa':
                        sortedImages.append(image)
                    elif images[n + 1][4] == 'retina':
                        if images[n - 1][4] == 'retina':
                            image[4] = 'rosa'
                            sortedImages.append(image)
                        elif images[n - 1][4] == 'rosa':
                            try:
                                if images[n + 2][4] == 'rosa':
                                    prevRosa = cv2.imread(images[n - 1][0], cv2.COLOR_BGR2GRAY)
                                    nextRosa = cv2.imread(images[n + 2][0], cv2.COLOR_BGR2GRAY)

                                    pCenter, pRadius, found = find_laser_spot_main_call(prevRosa)
                                    nCenter, nRadius, found = find_laser_spot_main_call(nextRosa)
                                    # If the difference between the two rosas is within 1%, we can copy it.
                                    if ((pCenter[0] - nCenter[0]) / nCenter[0]) * 100 < 1 and ((pCenter[1] - nCenter[1]) /
                                                                                               nCenter[1]) * 100 < 1:
                                        sortedImages.append(images[n - 2])
                                        sortedImages.append(image)
                                    else:
                                        # FIXME This might be problematic.
                                        sortedImages.append(['None', 0, 0, 0, 'rosa'])
                                        sortedImages.append(image)
                                else:
                                    image[4] = 'error'
                                    sortedImages.append(image)
                            except:
                                image[4] = 'error'
                                sortedImages.append(image)
                elif imType == 'rosa':
                    if images[n - 1][4] == 'retina':
                        sortedImages.append(image)
                    elif images[n - 1][4] == 'rosa':
                        if images[n + 1][4] == 'retina':
                            sortedImages.append(['None', 0, 0, 0, 'retina'])
                            sortedImages.append(image)
                        elif images[n + 1][4] == 'rosa':
                            image[4] = 'retina'
                            sortedImages.append(image)
                        else:
                            image[4] = 'error'
                            sortedImages.append(image)
                    else:
                        sortedImages.append(image)
                else:
                    sortedImages.append(image)
            else:
                sortedImages.append(image)

        return sortedImages

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

            retinas, rosas, erroneous = self.validateSorting(rows)
            pass

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
    def createMonkeysTable(dbPath: str, xlsxPath: str):
        with ZiliaDatabase(dbPath) as db:
            print('Changing to rwc mode...')
            db.changeConnectionMode('rwc')

            print('Putting Database in asynchronous mode... Only one person should proceed at once...')
            db.asynchronous()

            print("Dropping the monkeys table...")
            db.dropTable("monkeys")

            print('Reading the .xlsx file...')
            zixl = ZiliaXLSX(xlsxPath)
            keys = zixl.monkeyKeys()

            print('Setting up monkeys table...')
            db.setupMonkeysTable(keys)
        pass

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

            '''
            print("Querrying all series...")
            series = db.select('series')
            for serie in series:
                images = db.select('images', condition='"serie" IS "{}" ORDER BY "images" ASC'.format(serie['name']))
                db.setupTripletsTable(images)
            '''

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