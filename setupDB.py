from database.ziliaDB import ZiliaDatabase
import os


if __name__ == '__main__':
    cwd = os.getcwd()
    dbPath = os.path.join(os.path.dirname(cwd), 'experiment1', 'zilia.db')
    defaultPath = os.path.normpath(dbPath)
    imagesPath = os.path.dirname(dbPath)
    db = ZiliaDatabase(defaultPath)
    db.createZiliaDB(defaultPath, imagesPath)
    db.createImagesTable(defaultPath)