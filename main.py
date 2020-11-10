from ziliaImage.imageAnalysis import ImageAnalysis
from database.ziliaDB import ZiliaDatabase

if __name__ == '__main__':
    db = ZiliaDatabase('C:\\zilia\\zilia.db')
    #db.createZiliaDB()
    #db.createImagesTable()
    zi = ImageAnalysis()

    rows = db.select('images', condition='"monkey" IS "singe22" AND "serie" is "20200303_081806_200-200-200-30"')
    zi.setReferences(rows)
    #zi.compareVersionsMultipleImages(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    zi.alignImagesV2(rows)


    #rows = db.select('images', condition='"monkey" IS "singe11" AND "serie" is "20200229_142737_150-200-150-30"')
    #zi.setReferences(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    #zi.alignImagesV1(rows)
