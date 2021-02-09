from database.ziliaDB import ZiliaDatabase


if __name__ == '__main__':
    #cwd = os.getcwd()
    #dbPath = os.path.join(os.path.dirname(cwd), 'experiment1', 'zilia.db')
    #defaultPath = os.path.normpath(dbPath)
    #imagesPath = os.path.dirname(dbPath)
    db = ZiliaDatabase('C:\\zilia\\zilia.db')
    #db.createZiliaDB('C:\\zilia\\zilia.db', 'C:\\zilia')
    db.createMonkeysTable('C:\\zilia\\zilia.db', 'C:\\zilia\\Monkey subjects information.xlsx')
    #db.createImagesTable('C:\\zilia\\zilia.db')
    #db.createTripletsTable(dbPath)
