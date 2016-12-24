import unittest

from computations.utils.TimeSeriesMerger import *


class TestTimeSeriesMerger(unittest.TestCase):

    def test_merge(self):
        lts = [[1, 20, 30, 4], [20, 30, 4], [30, 4], [20, 30]]
        print(lts)
        merged_lts = TimeSeriesMerger.optimal_roll(lts)
        print(merged_lts)
        l1 = list(np.mean(merged_lts, axis=0))
        l2 = [np.nan, np.nan, 27.5, 10.5]
        self.assertEqual(l1[-1], l2[-1])
        self.assertEqual(l1[-2], l2[-2])

        l1 = [1, 2, 3, 4]
        l2 = [0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0]
        a_, b_ = TimeSeriesMerger.find_index(l1, l2)
        self.assertListEqual(list(a_), [0, 0, 0, 0, 1, 2, 3, 4, 0, 0, 0, 0])
        self.assertEqual(b_, 4)