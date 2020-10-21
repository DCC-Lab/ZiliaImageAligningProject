from zipfile import ZipFile
from datetime import date
import sqlite3 as lite
import urllib.parse as parse
import pathlib
import os
import fnmatch
import re
from database import Database
from utilities import findFiles
from ziliaImages import ZiliaImages


class ZiliaDatabase(Database):
    def __init__(self, pathToDB=None):
        if pathToDB is None:
            path = self.defaultPath()
        else:
            path = pathToDB

        super().__init__(path)

    def defaultPath(self):
        return 'C:\\zilia\\zilia.db'

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
                zi = ZiliaImages()
                retinas, rosas = zi.sortRetinasAndRosas(jpgs)
                n = 0
                for rosa in rosas:
                    try:
                        print("Insertion....")
                        statement = 'INSERT OR REPLACE INTO "images" ({}) VALUES ("{}", "{}", "{}", "{}")'\
                            .format('"serie", "monkey", "retinas", "rosas"', row["name"], row["monkey"], retinas[n], rosa)
                        self.execute(statement)
                    except:
                        print("Failed!")
                    n += 1

    @staticmethod
    def createZiliaDB():
        # Path to the Zilia DB is :
        ziliaDBPath = 'C:\\zilia\\zilia.db'

        # Proceeding to creating the database...
        with ZiliaDatabase(ziliaDBPath) as db:
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
    def createImagesTable():
        # Path to the Zilia DB is :
        ziliaDBPath = 'C:\\zilia\\zilia.db'

        with ZiliaDatabase(ziliaDBPath) as db:
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
