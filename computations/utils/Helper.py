import numpy as np
from sklearn import linear_model

from TimeSeriesMerger import *
from computations.Constants import *


class Helper(object):

    @staticmethod
    def convert_to_seconds(milliseconds):
        return np.array([1e-3 * x for x in milliseconds])

    @staticmethod
    def get_last_time_wheel_is_in_front_of_ref(wheel_lap_times, ball_lap_time_in_front_of_ref):
        res = None
        for wheel_time_in_front_of_ref in wheel_lap_times:
            if wheel_time_in_front_of_ref < ball_lap_time_in_front_of_ref:
                res = wheel_time_in_front_of_ref
        return res

    @staticmethod
    def compute_diff(lap_times):
        return np.diff(np.array(lap_times))

    @staticmethod
    def get_inverse(x):
        return 1 / x

    # Example is list of size 160, L=80. We expect two lists of size 80.
    @staticmethod
    def split(list_, l):
        n = len(list_) / l
        for i in range(0, len(list_), n):
            yield list_[i:i + n]

    @staticmethod
    def perform_regression(x_values, y_values):
        clf = linear_model.LinearRegression()
        clf.fit(x_values.reshape(-1, 1), y_values.reshape(-1, 1))
        return clf

    @staticmethod
    def find_abs_start_index(speeds, mean_speeds):
        new_speeds, index_of_rev_start_abs = TimeSeriesMerger.find_index(speeds, mean_speeds)
        return index_of_rev_start_abs

    @staticmethod
    def detect_diamonds(distance_left):
        """beginning is assumed to be at the ref diamond. Ref diamond is FORWARD.
        8 diamonds in total. We consider 9 here just to have the modulo to 1 (close the loop).
        For example, if we have distance_left = 0.99, we consider it to be close to 1
        => First diamond should be hit. And not the last one equal to 7/8 = 0.875
        Ball is going anti-clockwise"""
        res_distance_left = distance_left % 1
        diamond_angles = np.cumsum(np.ones(9) * 1.0 / 8) - 1.0 / 8

        # 5 is a big value to be sure to be inside the bounds of diamond_types[]
        diamond_types = [Constants.DiamondType.FORWARD, Constants.DiamondType.BLOCKER] * 5
        distance_from_diamonds = np.array(diamond_angles - res_distance_left) ** 2
        index = np.argmin(distance_from_diamonds) + Constants.MOVE_TO_NEXT_DIAMOND
        return diamond_types[index]
