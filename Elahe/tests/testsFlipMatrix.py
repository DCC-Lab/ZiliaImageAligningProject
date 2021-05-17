import envtest
import numpy as np


class TestFlipMatrix(envtest.ZiliaTestCase):
    def testNumpyAllReturnsTrueWhenAllElementsAreNonZero(self):
        A = np.array([1, 2])
        B = np.array([2, 1])

        self.assertIsNotNone(A)
        self.assertTrue(A.all())
        self.assertTrue(B.all())

        C = np.array([0,1])
        self.assertFalse(C.all())

    def testNumpyAllIsNotForComparingArrays(self):
        A = np.array([1, 2])
        B = np.array([2, 1])

        self.assertFalse(A is B)
        for i in range(2):
            self.assertTrue(A[i] != B[i])
        
        # This does not compare all elements of A and B
        self.assertTrue(A.all() == B.all()) 

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
