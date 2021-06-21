import envtest
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from processImages import getFiles
import matplotlib.pyplot as plt
import numpy as np

"""
WARNING: this test file will use absolute paths for data, which are necessary
due to the large amount of data that will be analyzed. These HAVE to be changed
to the correct paths if run on another copmuter.
"""

listOfFolderPaths = []

# These ones are veryyyyy saturated
listOfFolderPaths.append(r"E:\Baseline3\Kenya 1512692\20210316-142504-kenya-od-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Kenya 1512692\20210316-145131-kenya-os-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Rwanda 1512436\20210317-092821-rwanda-od-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Rwanda 1512436\20210317-092951-rwanda-od-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-134930-somalie-od-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-134957-somalie-od-onh-rlp24")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-140843-somalie-os-onh-rlp24gooooodim")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-140927-somalie-os-onh-rlp24gooooodim")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-141034-somalie-os-onh-rlp24gooooodim")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-141109-somalie-os-onh-rlp24gooooodim")
listOfFolderPaths.append(r"E:\Baseline3\Somalie 1508202\20210317-141139-somalie-os-onh-rlp24gooooodim")
# listOfFolderPaths.append(r"")


# @envtest.skip("Will fail on other computers if path is not selected properly.")
class TestFindAverageThresholdHiBrightness(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testListOfFolderPaths(self):
        # print(listOfFolderPaths)
        self.assertTrue(len(listOfFolderPaths) > 0)

    def testGetFiles(self):
        eyesAndRosas = getFiles(listOfFolderPaths[0])
        # print(eyesAndRosas)
        self.assertTrue(len(eyesAndRosas) > 0)

    @envtest.skip("skip plots")
    def testPlotHistogram(self):
        fakeData = [1,1,1,1,2,2,3,3,4,4,4,5,5,6,6,7,7,8,9,7,8,9]
        plt.hist(fakeData, bins='auto')
        plt.show()

    def testGetMeanOfList(self):
        fakeData = [1,1,1,1,2,2,3,3,4,4,4,5,5,6,6,7,7,8,9,7,8,9]
        mean = np.mean(fakeData)
        # print(mean) #4.681818181818182

    def testGetMeanThresholdOfWholeFolder(self):
        pass


if __name__ == "__main__":
    envtest.main()
