from database.ziliaDB import ZiliaDatabase
import os


if __name__ == '__main__':
    defaultPath = os.path.normpath('C:\\zilia\\zilia.db')
    db = ZiliaDatabase(defaultPath)
    db.createZiliaDB(defaultPath)
    db.createImagesTable(defaultPath)