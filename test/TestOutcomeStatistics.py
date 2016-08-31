import unittest

from OutcomeStatistics import *


class TestOutcomeStatistics(unittest.TestCase):
    def test_outcomeStatistics(self):
        os = OutcomeStatistics.create([3, 26, 0, 32, 15])
        self.assertEqual(0.0, os['mean_number'])
        self.assertEqual(np.sqrt(10.0), os['std_deviation'])
