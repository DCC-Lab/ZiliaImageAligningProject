import envtest
import unittest
from spectrumAnalysis import mainAnalysis, bloodTest
from processImages import getFiles
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


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

    @envtest.skip("not useful anymore")
    def testImport(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        self.assertIsNotNone(features)

    # @envtest.skip("not useful anymore")
    # def setUp(self):
    #     # this will get executed before every test
    #     super().setUp()
    #     self.features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
    #                             refNameNothinInfront=refNameNothinInfront,
    #                             componentsSpectra=componentsSpectra)

    @envtest.skip("not useful anymore")
    def testDataReturnTypeIsNumpyArray(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        self.assertTrue(type(features) == np.ndarray)

    def testJustInitiatePCA(self):
        pca = PCA()
        self.assertTrue(True)

    @envtest.skip("not useful anymore")
    def testFitPCAToTheData(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        self.assertTrue(True)

    @envtest.skip("not useful anymore")
    def testGetNumberOfComponentsOnRLP2(self):
        features = mainAnalysis(darkRefPath2, spectrumPath2, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components with default PCA parameters

    @envtest.skip("not useful anymore")
    def testGetNumberOfComponentsOnRLP4(self):
        features = mainAnalysis(darkRefPath6, spectrumPath6, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components AGAIN with default PCA parameters

    @envtest.skip("old code jams")
    def testGetNumberOfComponentsOnRLP14(self):
        features = mainAnalysis(darkRefPath14, spectrumPath14, whiteRefName=whiteRefName,
                                refNameNothinInfront=refNameNothinInfront,
                                componentsSpectra=componentsSpectra)
        pca = PCA()
        pca.fit(features)
        # print(pca.n_components_)
        # We get 6 components AGAIN AGAIN with default PCA parameters



    def testFitPCA_BloodTest(self):
        refNameNothinInfront = r"./TestSpectrums/blood/int75_LEDON_nothingInFront.csv"
        whiteRefName = r"./TestSpectrums/blood/int75_WHITEREFERENCE.csv"
        spectrumPath = r"./TestSpectrums/blood/so66_int300_avg1_1.csv"
        darkRefPath = r"./TestSpectrums/blood/int300_LEDON_nothingInFront.csv"
        componentsSpectra = r"../_components_spectra.csv"
        _, absorbance = bloodTest(refNameNothinInfront=refNameNothinInfront,
                                whiteRefName=whiteRefName, spectrumPath=spectrumPath,
                                darkRefPath=darkRefPath, componentsSpectra=componentsSpectra)
        data = absorbance.data
        pca = PCA()
        pca.fit(data)

    def testGetPCAExplainedVarianceRatio_BloodTest(self):
        refNameNothinInfront = r"./TestSpectrums/blood/int75_LEDON_nothingInFront.csv"
        whiteRefName = r"./TestSpectrums/blood/int75_WHITEREFERENCE.csv"
        spectrumPath = r"./TestSpectrums/blood/so66_int300_avg1_1.csv"
        darkRefPath = r"./TestSpectrums/blood/int300_LEDON_nothingInFront.csv"
        componentsSpectra = r"../_components_spectra.csv"
        _, absorbance = bloodTest(refNameNothinInfront=refNameNothinInfront,
                                whiteRefName=whiteRefName, spectrumPath=spectrumPath,
                                darkRefPath=darkRefPath, componentsSpectra=componentsSpectra)
        data = absorbance.data
        pca = PCA()
        pca.fit(data)
        varianceRatio = pca.explained_variance_ratio_
        self.assertIsNotNone(varianceRatio)

    @envtest.skip("skip plots")
    def testPlotPCAExplainedVarianceRatio_BloodTest(self):
        refNameNothinInfront = r"./TestSpectrums/blood/int75_LEDON_nothingInFront.csv"
        whiteRefName = r"./TestSpectrums/blood/int75_WHITEREFERENCE.csv"
        spectrumPath = r"./TestSpectrums/blood/so66_int300_avg1_1.csv"
        darkRefPath = r"./TestSpectrums/blood/int300_LEDON_nothingInFront.csv"
        componentsSpectra = r"../_components_spectra.csv"
        _, absorbance = bloodTest(refNameNothinInfront=refNameNothinInfront,
                                whiteRefName=whiteRefName, spectrumPath=spectrumPath,
                                darkRefPath=darkRefPath, componentsSpectra=componentsSpectra)
        data = absorbance.data.T
        print(data.shape)
        plt.plot(data.T)
        plt.show()
        pca = PCA(n_components=5)
        pca.fit(data)
        plt.plot(pca.components_.T)
        plt.show()
        varianceRatio = pca.explained_variance_ratio_
        plt.plot(varianceRatio, "b.")
        plt.show()

    def testLoadingASpectraFile(self):
        spectraDirectory = r"./TestSpectrums/rawRosaSpectraFromBaseline3"
        spectraPath = getFiles(spectraDirectory, "csv", newImages=False)[0]
        eyeSpectra = pd.read_csv(spectraPath)
        eyeSpectra = eyeSpectra.drop([0,1,2]) # to remove first junk lines
        eyeSpectra = eyeSpectra.drop(columns=["wavelength", "ref", "bg"])
        self.assertIsNotNone(eyeSpectra)
        # print(eyeSpectra)

    def testCastingASpectraFileToNumpyArray(self):
        spectraDirectory = r"./TestSpectrums/rawRosaSpectraFromBaseline3"
        spectraPath = getFiles(spectraDirectory, "csv", newImages=False)[0]
        eyeSpectra = pd.read_csv(spectraPath)
        eyeSpectra = eyeSpectra.drop([0,1,2]) # to remove the first junk lines
        eyeSpectra = eyeSpectra.drop(columns=["wavelength", "ref", "bg"])
        eyeSpectra = eyeSpectra.to_numpy()
        self.assertIsNotNone(eyeSpectra)
        self.assertTrue(type(eyeSpectra) == np.ndarray)
        # print(eyeSpectra)

    @envtest.skip("skip plots")
    def testPCAOn1SpectrumFile(self):
        spectraDirectory = r"./TestSpectrums/rawRosaSpectraFromBaseline3"
        spectraPath = getFiles(spectraDirectory, "csv", newImages=False)[0]
        eyeSpectra = pd.read_csv(spectraPath)
        eyeSpectra = eyeSpectra.drop([0,1,2]) # to remove the first junk lines
        eyeSpectra = eyeSpectra.drop(columns=["wavelength", "ref", "bg"])
        eyeSpectra = eyeSpectra.to_numpy().T
        data = eyeSpectra
        print(data.shape)
        plt.plot(data.T)
        plt.show()
        # pca = PCA()
        pca = PCA(n_components=5)
        pca.fit(data)
        plt.plot(pca.components_.T)
        plt.show()
        varianceRatio = pca.explained_variance_ratio_
        plt.plot(varianceRatio, "b.")
        plt.show()


    def loadAllSpectrumFiles(self, spectraDirectory):
        spetraPaths = getFiles(spectraDirectory, "csv", newImages=False)
        data = None
        for spectraPath in spectraPaths:
            eyeSpectra = pd.read_csv(spectraPath)
            eyeSpectra = eyeSpectra.drop([0,1,2]) # to remove the first junk lines
            eyeSpectra = eyeSpectra.drop(columns=["wavelength", "ref", "bg"])
            eyeSpectra = eyeSpectra.to_numpy().T
            if data is None:
                # for the first iteration
                data = eyeSpectra
            else:
                data = np.hstack((data, eyeSpectra))
        return data






    @envtest.skip("not finished yet")
    def testPlotLotsOfRosaSpectraExplainedVarianceRatio(self):
        spectraDirectory = r"./TestSpectrums/rawRosaSpectraFromBaseline3"
        data = self.loadAllSpectrumFiles(spectraDirectory)
        print(data.shape)
        plt.plot(data.T)
        plt.show()
        pca = PCA(n_components=5)
        pca.fit(data)
        plt.plot(pca.components_.T)
        plt.show()
        varianceRatio = pca.explained_variance_ratio_
        plt.plot(varianceRatio, "b.")
        plt.show()


if __name__ == "__main__":
    envtest.main()
