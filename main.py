from ziliaImage.imageanalysis import ImageAnalysis
from ziliaImage.imageanalytics import ImageAnalytics
from database.ziliaDB import ZiliaDatabase

if __name__ == '__main__':
    db = ZiliaDatabase('C:\\zilia\\zilia.db')

    rows = db.select('images', condition='"monkey" IS "singe22" AND "serie" is "20200303_081806_200-200-200-30"')
    zi = ImageAnalysis(rows)
    zi.alignImages(makeGraph=True, makeStack=True)
    #zi.setReferences(rows)
    #zi.compareVersionsMultipleImages(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    #zi.testBadDetectionV2(rows)
    #zi.testClusteringV2(rows)

    #rows = db.select('images', condition='"monkey" IS "singe11" AND "serie" is "20200229_142737_150-200-150-30"')
    #zi = ImageAnalytics(rows)
    #zi.compareVersionsMultipleImages(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    #zi.testClusteringV2(rows)
    #zi.testBadDetectionV2()
