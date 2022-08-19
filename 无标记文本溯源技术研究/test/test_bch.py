import unittest
import sys
import random
import numpy as np

sys.path.append("../src")
import bch

class TestBch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        cls.example_short = np.array([0,1,1,0])
        cls.example_long = np.array([1,0,0,1,0,0,1,0,1])
        cls.example_1 = np.array([0,1,0,0,0,1,0])
        cls.example_2 = np.array([0,0,0,1,0,1,1])
    
    def test_case_fail(self):

        with self.assertRaises(AssertionError):
            bch.bchEncode(self.example_short)

        with self.assertRaises(AssertionError):
            bch.bchEncode(self.example_long)

    def test_case_1(self):
        test_1 = bch.bchEncode(self.example_1)
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_1, np.array([0,1,0,0,0,1,0,0,0,0,0,0,1,1,1]))]), 0)

        # zero mistake
        self.assertTrue(bch.bchDecode(test_1))

        # one mistake
        bit = random.randint(0, 14)
        test_1[bit] = 1 - test_1[bit]
        self.assertTrue(bch.bchDecode(test_1))  # correct
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_1, np.array([0,1,0,0,0,1,0,0,0,0,0,0,1,1,1]))]), 0)

        # two mistake
        bit1 = random.randint(0, 14)
        bit2 = random.randint(0, 14)
        while bit2 == bit1:
            bit2 = random.randint(0, 14)
        test_1[bit1] = 1 - test_1[bit1]
        test_1[bit2] = 1 - test_1[bit2]
        self.assertTrue(bch.bchDecode(test_1))  # correct
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_1, np.array([0,1,0,0,0,1,0,0,0,0,0,0,1,1,1]))]), 0)
        
    def test_case_2(self):
        test_2 = bch.bchEncode(self.example_2)
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_2, np.array([0,0,0,1,0,1,1,1,0,1,1,1,1,1,1]))]), 0)

        # zero mistake
        self.assertTrue(bch.bchDecode(test_2))

        # one mistake
        bit = random.randint(0, 14)
        test_2[bit] = 1 - test_2[bit]
        self.assertTrue(bch.bchDecode(test_2))  # correct
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_2, np.array([0,0,0,1,0,1,1,1,0,1,1,1,1,1,1]))]), 0)

        # two mistake
        bit1 = random.randint(0, 14)
        bit2 = random.randint(0, 14)
        while bit2 == bit1:
            bit2 = random.randint(0, 14)
        test_2[bit1] = 1 - test_2[bit1]
        test_2[bit2] = 1 - test_2[bit2]
        self.assertTrue(bch.bchDecode(test_2))  # correct
        self.assertEqual(sum([a ^ b for (a, b) in zip(test_2, np.array([0,0,0,1,0,1,1,1,0,1,1,1,1,1,1]))]), 0)



if __name__ == '__main__':
    unittest.main()