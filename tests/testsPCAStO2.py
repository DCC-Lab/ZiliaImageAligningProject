import envtest
import unittest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA
import numpy as np


# Run tests in order they are written
unittest.TestLoader.sortTestMethodsUsing = None

# These 2 will always be the same for every test
whiteRefName = r"./TestSpectrums/int75_WHITEREFERENCE.csv"
refNameNothinInfront = r"./TestSpectrums/int75_LEDON_nothingInFront.csv"
componentsSpectra = r'./TestSpectrums/_components_spectra.csv'

# These will be different for every test
darkRefPath = r"./TestSpectrums/bresilODrlp2/background.csv"
spectrumPath = r"./TestSpectrums/bresilODrlp2/spectrum.csv"


class TestPCAStO2(envtest.ZiliaTestCase):

    def testImport(self):
        features = mainAnalysis(darkRefPath, spectrumPath, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        self.assertIsNotNone(features)

    def setUp(self):
        # this will get executed before every test
        super().setUp()
        self.features = mainAnalysis(darkRefPath, spectrumPath, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)

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
