import sys
import unittest


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/predictor")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from test.OutcomeStatisticsTest import OutcomeStatisticsTest
from test.RegressionTest import RegressionTest
from test.TestWheel import TestWheel

from test.TestHelper import TestHelper


def test_list():
    return [TestWheel,
            RegressionTest,
            TestHelper,
            OutcomeStatisticsTest]


def run_test():
    for test_class in test_list():
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == '__main__':
    run_test()
