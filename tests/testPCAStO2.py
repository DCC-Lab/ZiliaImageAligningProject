import envtest
from spectrumAnalysis import mainAnalysis
from sklearn.decomposition import PCA

# referenceNameNothinInfront=r"./int75_LEDON_nothingInFront.csv", whiteReferenceName = r"./int75_WHITEREFERENCE.csv"

class TestPCAStO2(envtest.ZiliaTestCase):

    def testImport(self):
        pass

        # features = mainAnalysis()
        # pca = PCA()
        # pca.fit
        # print(pca.components_)

        # pca = PCA(n_components=2)
        # print(pca.components_)

if __name__ == "__main__":
    envtest.main()
