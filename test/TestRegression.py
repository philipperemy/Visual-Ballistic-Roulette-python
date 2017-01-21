import unittest

from computations.comp_utils.Helper import *


class TestRegression(unittest.TestCase):
    def test_regression(self):
        x = np.array([1, 3, 4])
        y = np.array([1, 3, 4])

        regression = Helper.perform_regression(x, y)
        self.assertEqual(regression.coef_, 1.0)
        self.assertEqual(regression.intercept_, 0.0)
