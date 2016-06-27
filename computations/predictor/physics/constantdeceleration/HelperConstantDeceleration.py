from Helper import *
from utils.Exceptions import *


class HelperConstantDeceleration(object):
    #  We should be able to average the deceleration factor. The intercept should not change.
    @staticmethod
    def estimate_time(constant_deceleration_model, current_revolution, revolution_count_left):
        revolution_count_floor = int(np.floor(revolution_count_left))

        if revolution_count_floor > 100:
            raise CriticalException()

        remaining_time = 0.0
        i = 1
        while i <= revolution_count_floor:
            speed_forecast = constant_deceleration_model.predict(current_revolution + i)[0, 0]
            remaining_time += Helper.get_time_for_one_ball_loop(speed_forecast)
            i += 1

        revolution_count_residual = revolution_count_left - revolution_count_floor
        speed_1 = constant_deceleration_model.predict(current_revolution + revolution_count_floor)[0, 0]
        speed_2 = constant_deceleration_model.predict(current_revolution + revolution_count_floor + 1)[0, 0]
        avg_speed_last_rev = (1 - revolution_count_residual) * speed_1 + revolution_count_residual * speed_2

        if avg_speed_last_rev < 0.0:
            raise PositiveValueExpectedException()

        remaining_time += revolution_count_residual * Helper.get_time_for_one_ball_loop(avg_speed_last_rev)
        return remaining_time

    @staticmethod
    def estimate_revolution_count_left(constant_deceleration_model, current_revolution, cutoff_speed):
        slope = constant_deceleration_model.coef_[0, 0]
        intercept = constant_deceleration_model.intercept_[0]
        revolution_count_left = (cutoff_speed - intercept) / slope - current_revolution
        if revolution_count_left < 0:
            raise PositiveValueExpectedException()
        return revolution_count_left

    @staticmethod
    def compute_model(diff_times, slope=None):
        x = np.array(range(1, len(diff_times) + 1, 1))  # [1, 2, 3, ..., size_of_speeds_array]
        speeds = np.apply_along_axis(func1d=Helper.get_ball_speed, axis=0, arr=diff_times)
        if slope is None:
            return Helper.perform_regression(x, speeds)
        else:
            # http://stackoverflow.com/questions/33292969/linear-regression-with-specified-slope
            intercept = np.mean(speeds - slope * x)
            return Helper.perform_regression(x, slope * x + intercept)  # trick
