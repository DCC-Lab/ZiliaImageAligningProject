import envtest  # modifies path
from utilities import *

class TestUtilities(envtest.ZiliaTestCase):

    def testFindAnyFiles(self):
        files = findFiles(directory=".", extension="*")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 3)

    def testFindPythonFiles(self):
        # I read the documentation for fnmatch, and 
        # findFiles should rename its extension argument "pattern"
        # https://docs.python.org/3/library/fnmatch.html
        files = findFiles(directory=".", extension="*.py")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 3)

    def testFindTestFiles(self):
        files = findFiles(directory=".", extension="test*.py")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 2)

    def testFindDirectories(self):
        # We are in a "tests/" directory, but the function only returns files
        files = findFiles(directory="../", extension="tests")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 0)

    def testConfirmFindDirectoriesOnly(self):
        files = findFiles(directory="../", extension="*")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) >= 10) # Lots of files here
        for file in files:
            self.assertTrue(os.path.exists(file))
            self.assertFalse(os.path.isdir(file))

    def testFindFilesInDirectories(self):
        # We are in a "tests/" directory, but the function only returns files
        # it only matches the file name too
        files = findFiles(directory="../", extension="tests*py")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) >= 2)

    def testFindFilesMatchDirectoryName(self):
        # We are in a "tests/" directory, but the function only returns files
        # it only matches the file name too
        files = findFiles(directory="../", extension="obsolete")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) >= 0)

if __name__ == '__main__':
    envtest.main()
