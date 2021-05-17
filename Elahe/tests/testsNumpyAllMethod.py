import envtest
import numpy as np


class TestNumpyAllMethod(envtest.ZiliaTestCase):
    def testNumpyAll(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertFalse(A is B)

    def testNumpyArraysNotEqualButTheAllMethodReturnsEqual(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertIsNotNone(B)
        for i in range(2):
            self.assertTrue(A[i] != B[i])
        self.assertTrue(A.all() == B.all())

    def testNumpyAllIsNotTheSumOfTheArrayValues(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        B = np.array([2, 1])
        self.assertIsNotNone(B)
        sumA = []
        sumB = []
        for i in range(2):
            sumA.append(A[i])
            sumB.append(B[i])
        self.assertTrue( sum(sumA) == sum(sumB) )
        self.assertFalse(A.all() == sum(sumA))
        #print(type(A.all())) # retourne un 'numpy.bool'

    def testNumpyAllReturnsABool(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        # print(type(A.all())) # retourne un 'numpy.bool'
        self.assertTrue(type(A.all()) == np.bool_)

    def testNumpyAllJustChecksIfValueIsZeroOrNot(self):
        A = np.array([1, 2])
        self.assertIsNotNone(A)
        C = np.array([0, 1])
        self.assertIsNotNone(C)
        self.assertFalse(A.all() == C.all())
        self.assertFalse(C.all())
        self.assertTrue(A.all())


if __name__ == '__main__':
    envtest.main()
