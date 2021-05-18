import cv2
import os
from ziliaImages import ZiliaImages
from ziliaDB import ZiliaDatabase
import numpy as np


if __name__ == '__main__':
    zi = ZiliaImages()
    db = ZiliaDatabase()
    #db.createZiliaDB()
    #db.createImagesTable()
    rows = db.select('images', condition='"monkey" IS "singe22" AND "serie" is "20200303_081806_200-200-200-30"')
    zi.alignImages(rows)
