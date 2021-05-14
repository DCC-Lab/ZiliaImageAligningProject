import envtest
import numpy as np


class TestFlipMatrix(envtest.ZiliaTestCase):
    def testNumpyAll(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertFalse(A is B)
        for i in range(2):
            self.assertTrue(A[i] != B[i])
        self.assertTrue(A.all() == B.all())
        sumA = []
        sumB = []
        for i in range(2):
            sumA.append(A[i])
            sumB.append(B[i])
        sumA = sum(sumA)
        sumB = sum(sumB)
        self.assertTrue(sumA == sumB)
        C = np.array([0,1])
        self.assertFalse(A.all() == C.all())
        self.assertFalse(C.all())
        self.assertTrue(A.all())
        # self.assertTrue(A.all() == sumA)
        #print(type(A.all())) # retourne un 'numpy.bool'

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
