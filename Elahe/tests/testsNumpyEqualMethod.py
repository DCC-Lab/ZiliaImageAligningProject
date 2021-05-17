import envtest
import numpy as np


class TestNumpyEqualMethod(envtest.ZiliaTestCase):
    def testReturnTypeOfEqualMethod(self):
        A = [1,2]
        self.assertIsNotNone(A)
        B = [2,1]
        self.assertIsNotNone(B)
        self.assertTrue(type(np.equal(A, B)) == np.ndarray)
        # print(type(np.equal(A,B)))
        # print(np.equal(A,B))
        # print(np.equal(A,A))

    def testEqualMethodWorksWithNumpyArrays(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertIsNotNone(B)
        self.assertTrue(type(np.equal(A, B)) == np.ndarray)

    def testEqualMethodReturnsAMatrix(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertIsNotNone(B)
        M = np.equal(A, B)
        self.assertIsNotNone(M)
        self.assertTrue(type(M) == np.ndarray)

    def testEqualMethodReturnsBoolElements(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertIsNotNone(B)
        M = np.equal(A, B)
        self.assertIsNotNone(M)
        for i in range(2):
            self.assertTrue(type(M[i]) == np.bool_)

    def testEqualMethodWorksWith2DMatrices(self):
        A = np.array([[1, 2], [3, 4]])
        self.assertIsNotNone(A)
        B = np.array([[2, 1], [4,3]])
        self.assertIsNotNone(B)
        M = np.equal(A, B)
        self.assertIsNotNone(M)



if __name__ == '__main__':
    envtest.main()
