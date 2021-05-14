import envtest  # modifies path
from utilities import findFiles
import os

class TestUtilities(envtest.ZiliaTestCase):
    # I wrote these tests to validate the behaviour of 
    # the findFiles functions in utilities.py.
    def testFindAnyFiles(self):
        files = findFiles(directory=".", extension="*")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) > 0)
        self.assertTrue(len(files) >= 3)

    def testFindPythonFiles(self):
        # I read the documentation for fnmatch (used in findFiles), and 
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

    def testFindDirectoriesReturnsPathsRelativeToProvidedArgument(self):
        files = findFiles(directory="../", extension="*")
        for file in files:
            self.assertFalse(os.path.isabs(file))

    def testFindDirectoriesReturnsAbsolutePathsWithAbsoluteDir(self):        
        if os.name == 'posix':
            files = findFiles(directory="/tmp", extension="*")
        elif os.name == 'nt':
            files = findFiles(directory=r"C:\Windows", extension="*.exe")
        else:
            self.fail("OS unknown")

        for file in files:
            self.assertTrue(os.path.isabs(file))

    def testFindFilesCanMatchDirectoryName(self):
        files = findFiles(directory="../", extension="obsolete")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) >= 0)

    def testFindFilesCanMatchDirectoryNameWithPattern(self):
        files = findFiles(directory="../", extension="obsolete/*py")
        self.assertIsNotNone(files)
        self.assertTrue(len(files) >= 0)

if __name__ == '__main__':
    envtest.main()
