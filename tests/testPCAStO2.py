import envtest
import unittest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA
import numpy as np


# Run tests in order they are written
unittest.TestLoader.sortTestMethodsUsing = None

componentsSpectra = r'./TestSpectrums/_components_spectra.csv'
darkRefPath = r"./TestSpectrums/background.csv"
spectrumPath = r"./TestSpectrums/spectrum.csv"
refNameNothinInfront = r"./TestSpectrums/int75_LEDON_nothingInFront.csv"
whiteRefName = r"./TestSpectrums/int75_WHITEREFERENCE.csv"


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
