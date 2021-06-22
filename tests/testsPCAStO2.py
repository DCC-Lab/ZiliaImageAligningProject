import envtest
import unittest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA
import numpy as np


# Run tests in order they are written
unittest.TestLoader.sortTestMethodsUsing = None

<<<<<<< HEAD
# These 3 will always be the same for every test
whiteRefName = r"../int75_WHITEREFERENCE.csv"
refNameNothinInfront = r"../int75_LEDON_nothingInFront.csv"
componentsSpectra = r'../_components_spectra.csv'

# These will be different for every test
darkRefPath2 = r"./TestSpectrums/bresilODrlp2/background.csv"
spectrumPath2 = r"./TestSpectrums/bresilODrlp2/spectrum.csv"
darkRefPath6 = r"./TestSpectrums/bresilODrlp6/background.csv"
spectrumPath6 = r"./TestSpectrums/bresilODrlp6/spectrum.csv"
darkRefPath14 = r"./TestSpectrums/bresilODrlp14/background.csv"
spectrumPath14 = r"./TestSpectrums/bresilODrlp14/spectrum.csv"
=======
componentsSpectra = r'./TestSpectrums/_components_spectra.csv'
darkRefPath = r"./TestSpectrums/background.csv"
spectrumPath = r"./TestSpectrums/spectrum.csv"
refNameNothinInfront = r"./TestSpectrums/int75_LEDON_nothingInFront.csv"
whiteRefName = r"./TestSpectrums/int75_WHITEREFERENCE.csv"
>>>>>>> 1b140f2c9db1f809a257ce0c64433233557399d9


class TestPCAStO2(envtest.ZiliaTestCase):

    def testImport(self):
        features = mainAnalysis(refNameNothinInfront, whiteRefName, darkRefPath, spectrumPath, componentsSpectra)
        self.assertIsNotNone(features)

    def setUp(self):
        # this will get executed before every test
        super(TestPCAStO2, self).setUp()
        self.features = mainAnalysis(refNameNothinInfront, whiteRefName, darkRefPath, spectrumPath, componentsSpectra)

    def testDataReturnTypeIsNumpyArray(self):
        self.assertTrue(type(self.features) == np.ndarray)

    def testJustInitiatePCA(self):
        pca = PCA()
        self.assertTrue(True)

    def testFitPCAToTheData(self):
        pca = PCA()
        pca.fit(self.features)
        self.assertTrue(True)

    def testGetNumberOfComponents(self):
        pca = PCA()
        pca.fit(self.features)
        # print(pca.n_components_)
        # We get 6 components with default PCA parameters

if __name__ == "__main__":
    envtest.main()
