from ziliaImage.imageAnalysis import ImageAnalysis
from database.ziliaDB import ZiliaDatabase

if __name__ == '__main__':
    db = ZiliaDatabase()
    #db.createZiliaDB()
    #db.createImagesTable()
    rows = db.select('images', condition='"monkey" IS "singe22" AND "serie" is "20200303_081806_200-200-200-30"')

    zi = ImageAnalysis()
    zi.setReferences(rows)
    #zi.compareFindLaserSpotOneImage(zi.rosaRef, 100)
    zi.compareFindLaserSpotMultipleImages(rows)
    #zi.alignImages(rows)
