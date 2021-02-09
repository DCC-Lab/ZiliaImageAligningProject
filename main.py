from ziliaImage.imageanalysis import ImageAnalysis
from ziliaImage.imageanalytics import ImageAnalytics
from database.ziliaDB import ZiliaDatabase
import os
import re

if __name__ == '__main__':
    #cwd = os.getcwd()
    #dbPath = os.path.join(os.path.dirname(cwd), 'experiment1', 'zilia.db')
    #db = ZiliaDatabase(dbPath)
    #rows = db.select('series', condition='"type" IS NOT "darkref"')
    #for row in rows:
    #    images = db.select('images', condition='"serie" is {}'.format(row['name']))
    #    zi = ImageAnalysis(images)
    #    zi.alignImages()

    path = os.path.normpath('C:\\zilia\\zilia.db')
    db = ZiliaDatabase(path)
    rows = db.select('images', condition='"monkey" IS "singe22" AND "serie" is "20200303_081806_200-200-200-30"')
    zi = ImageAnalysis(rows)
    zi.alignImages(makeGraph=True)

    #rows = db.select('images', condition='"monkey" IS "singe34" AND "serie" is "20200304_091936_psr_rlp70"')
    #zi = ImageAnalysis(rows)
    #zi.alignImages(makeGraph=True)
    #zi.setReferences(rows)
    #zi.compareVersionsMultipleImages(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    #zi.testBadDetectionV2(rows)
    #zi.testClusteringV2(rows)

    #rows = db.select('images', condition='"monkey" IS "singe11" AND "serie" is "20200229_142737_150-200-150-30"')
    #zi = ImageAnalysis(rows)
    #zi.alignImages(makeGraph=True)
    #zi.compareVersionsMultipleImages(rows)
    #zi.compareVersionsHistogram(rows)
    #zi.compareVersionsHistogram2D(rows, True)
    #zi.testClusteringV2(rows)
    #zi.testBadDetectionV2()

