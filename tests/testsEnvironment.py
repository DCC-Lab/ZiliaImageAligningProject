import envtest  # modifies path
import matplotlib.pyplot as plt
import sys

class TestEnvironment(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

    def testPath(self):
        import utilities
        # if path is incorrect, this will throw an exception


if __name__ == '__main__':
    envtest.main()
