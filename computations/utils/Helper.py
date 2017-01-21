import numpy as np
from sklearn import linear_model

from computations.utils.TimeSeriesMerger import TimeSeriesMerger as tsm


class Helper(object):
    @staticmethod
    def convert_to_seconds(milliseconds):
        return 1e-3 * np.array(milliseconds)

    @staticmethod
    def get_last_time_wheel_is_in_front_of_ref(wheel_lap_times, ball_lap_time_in_front_of_ref):
        res = None
        for wheel_time_in_front_of_ref in wheel_lap_times:
            if wheel_time_in_front_of_ref < ball_lap_time_in_front_of_ref:
                res = wheel_time_in_front_of_ref
        return res

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
    def find_abs_start_index(times, mean_times):
        new_times, index_of_rev_start_abs = tsm.find_index(times, mean_times)
        return index_of_rev_start_abs
