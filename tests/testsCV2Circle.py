import envtest
from cv2 import circle

class TestCV2Circle(envtest.ZiliaTestCase):

    def testInit(self):
        self.assertTrue(True)

if __name__ == "__main__":
    envtest.main()
