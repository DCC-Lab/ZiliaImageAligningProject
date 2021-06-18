import envtest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA

componentsSpectra = r'./TestSpectrums/_components_spectra.csv'
darkRefPath = r"./TestSpectrums/background.csv"
spectrumPath = r"./TestSpectrums/spectrum.csv"
referenceNameNothinInfront=r"./TestSpectrums/int75_LEDON_nothingInFront.csv"
whiteReferenceName = r"./TestSpectrums/int75_WHITEREFERENCE.csv"


class TestPCAStO2(envtest.ZiliaTestCase):

    def testImport(self):
        features = mainAnalysis(referenceNameNothinInfront, whiteReferenceName, darkRefPath, spectrumPath, componentsSpectra)
        self.assertIsNotNone

        # features = mainAnalysis()
        # pca = PCA()
        # pca.fit
        # print(pca.components_)

        # pca = PCA(n_components=2)
        # print(pca.components_)

if __name__ == "__main__":
    envtest.main()
