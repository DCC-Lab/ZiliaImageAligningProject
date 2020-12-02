from database.ziliaDB import ZiliaDatabase
import os


if __name__ == '__main__':
    defaultPath = os.path.normpath('\\experiment1\\zilia.db')
    imagesPath = os.path.normpath('\\experiment1')
    db = ZiliaDatabase(defaultPath)
    db.createZiliaDB(defaultPath, imagesPath)
    db.createImagesTable(defaultPath)