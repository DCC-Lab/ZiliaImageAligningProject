import envtest
import unittest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA
import numpy as np


# Run tests in order they are written
unittest.TestLoader.sortTestMethodsUsing = None

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


class TestPCAStO2(envtest.ZiliaTestCase):

    def testImport(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        self.assertIsNotNone(features)

    def setUp(self):
        # this will get executed before every test
        super().setUp()
        self.features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)

    def testDataReturnTypeIsNumpyArray(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        self.assertTrue(type(features) == np.ndarray)

    def testJustInitiatePCA(self):
        pca = PCA()
        self.assertTrue(True)

    def testFitPCAToTheData(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        self.assertTrue(True)

    def testGetNumberOfComponentsOnRLP2(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components with default PCA parameters

    def testGetNumberOfComponentsOnRLP4(self):
        features = mainAnalysis(darkRefPath6, spectrumPath6, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components AGAIN with default PCA parameters

    def testGetNumberOfComponentsOnRLP14(self):
        features = mainAnalysis(darkRefPath14, spectrumPath14, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components AGAIN AGAIN with default PCA parameters


if __name__ == "__main__":
    envtest.main()
