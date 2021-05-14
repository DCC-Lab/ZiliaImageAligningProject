import envtest  # modifies path
from utilities import *

class TestUtilities(envtest.ZiliaTestCase):

    def testFindAnyFiles(self):
        files = findFiles(directory="./", extension="*")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 3)

    def testFindPythonFiles(self):
        files = findFiles(directory="./", extension="*")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 3)



if __name__ == '__main__':
    envtest.main()
