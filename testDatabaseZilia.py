import env
from dcclab.database import *
from datetime import date
from zilia import *
import unittest
import os
import numpy as np

dbPath = 'test.db'
ziliaDb = '/tmp/zilia.db'

class TestZilia(env.DCCLabTestCase):
    def testZiliaDBCreation(self):
        self.assertIsNotNone(ZiliaDB(ziliaDb))

    def testZiliaGetMonkeyNames(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        db.execute("select name from monkeys order by name")
        rows = db.fetchAll()
        self.assertTrue(len(rows) == 4)
        self.assertEqual([ r['name'] for r in rows], ['Bresil', 'Kenya', 'Rwanda', 'Somalie'])

    def testGetMonkeyNames(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        names = db.getMonkeyNames()
        self.assertEqual(names, ['Bresil', 'Kenya', 'Rwanda', 'Somalie'])

    def testGetWavelengths(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        wavelengths = db.getWavelengths()
        self.assertTrue(wavelengths.shape == (512,))

    def testGetAcquisitionType(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        types = db.getAcquisitionType()
        self.assertEqual(types, ['baseline'])

    def testGetColumns(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        cols = db.getColumns()
        self.assertEqual(cols, ['bg','raw','ref'])

    def testGetTargets(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        targets = db.getTargets()
        self.assertEqual(targets, ['mac','onh'])

    def testGetSpectra(self):
        db=ZiliaDB(ziliaDb)
        self.assertIsNotNone(db)
        spectra = db.getRawIntensities(monkey='Rwanda', target='onh', type='baseline', column='raw')
        self.assertIsNotNone(spectra)
        print(spectra.shape)

if __name__ == '__main__':
    unittest.main()
