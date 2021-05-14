import envtest
import numpy as np


class TestFlipMatrix(envtest.ZiliaTestCase):
    def testNumpyDiagonalMatrix(self):
        A = np.diag([1, 2, 3, 4, 5])
        self.assertIsNotNone(A)
        for i in range(5):
            for j in range(5):
                if i == j:
                    self.assertTrue(A[i,j] != 0)
                else:
                    self.assertTrue(A[i,j] == 0)

    def testNumpyFlipLRDiagonal(self):
        A = np.diag([1, 2, 3, 4, 5])
        self.assertIsNotNone(A)
        B = np.fliplr(A)
        self.assertIsNotNone(B)
        # self.assertTrue(A.all() == B.all())

    def testNumpyFlipLRArbitrary(self):
        A = np.array([[1, 2],[3,4]])
        self.assertIsNotNone(A)
        B = np.fliplr(A)
        self.assertIsNotNone(B)
        self.assertEqual(B[0,0], 2)
        self.assertEqual(B[0,1], 1)
        self.assertEqual(B[1,0], 4)
        self.assertEqual(B[1,1], 3)


if __name__ == '__main__':
    envtest.main()
