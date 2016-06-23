import numpy as np
from sklearn import linear_model

from Constants import *
from Exceptions import *


class Helper(object):
    @staticmethod
    def convert_to_seconds(milliseconds):
        return [1e-3 * x for x in milliseconds]

    @staticmethod
    def print_val_or_infinity_symbol(value):
        return "+oo" if value > 1e9 else str(value)

    @staticmethod
    def get_last_time_wheel_is_in_front_of_ref(wheel_lap_times, ball_lap_time_in_front_of_ref):
        # index starts at 0.
        idx = np.sum(np.array(wheel_lap_times < ball_lap_time_in_front_of_ref, dtype=int)) - 1
        return wheel_lap_times[idx]

    @staticmethod
    def compute_diff(lap_times):
        return np.diff(lap_times)

    @staticmethod
    def normalize(cumsum_times, origin):
        return cumsum_times - origin

    @staticmethod
    def estimate_distance_constant_speed(t1, t2, speed):
        return speed * (t2 - t1)

    #  m/s
    @staticmethod
    def get_ball_speed(t1, t2=0):
        return Constants.get_ball_circumference() / abs(t2 - t1)

    #  m/s
    @staticmethod
    def get_wheel_speed(t1, t2=0):
        return Constants.get_wheel_circumference() / abs(t2 - t1)

    @staticmethod
    def get_time_for_one_ball_loop(ball_speed):
        return Constants.get_ball_circumference() / ball_speed

    #  Could interpolate with ML stuffs.
    @staticmethod
    def get_time_for_one_wheel_loop(wheel_speed):
        return Constants.get_wheel_circumference() / wheel_speed

    #  m/s. T1 and T2
    @staticmethod
    def get_speed(t1, t2, i_type):
        if i_type == Constants.Type.BALL:
            return Helper.get_ball_speed(t1, t2)
        elif i_type == Constants.Type.WHEEL:
            return Helper.get_wheel_speed(t1, t2)
        else:
            raise CriticalException("Unknown type.")

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
