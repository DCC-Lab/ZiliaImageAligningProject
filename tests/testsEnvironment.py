import envtest  # modifies path
import sys

class TestEnvironment(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testPath(self):
        import processImages
        # if path is incorrect, this will throw an exception

    def testPythonVersion(self):
        self.assertTrue(sys.version_info.major == 3)
        self.assertTrue(sys.version_info.minor >= 8)

if __name__ == '__main__':
    envtest.main()
