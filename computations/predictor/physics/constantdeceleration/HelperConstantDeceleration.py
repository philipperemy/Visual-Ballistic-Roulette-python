from scipy.interpolate import interp1d

from TimeSeriesMerger import *


class HelperConstantDeceleration(object):
    @staticmethod
    def estimate_time_2(speeds_mean, index_start_of_speeds_mean, current_revolution, revolution_count_left):
        revolution_count_floor = int(np.floor(revolution_count_left))

        if revolution_count_floor > 100:
            raise CriticalException()

        remaining_time = 0.0
        i = 1
        while i <= revolution_count_floor:
            speed_forecast = speeds_mean[index_start_of_speeds_mean + current_revolution + i]
            remaining_time += Helper.get_time_for_one_ball_loop(speed_forecast)
            i += 1

        revolution_count_residual = revolution_count_left - revolution_count_floor
        speed_1 = speeds_mean[index_start_of_speeds_mean + current_revolution + revolution_count_floor]

        last_index = index_start_of_speeds_mean + current_revolution + revolution_count_floor + 1
        if last_index >= len(speeds_mean):
            speed_2 = speed_1
        else:
            speed_2 = speeds_mean[last_index]
        avg_speed_last_rev = (1 - revolution_count_residual) * speed_1 + revolution_count_residual * speed_2

        if avg_speed_last_rev < 0.0:
            raise PositiveValueExpectedException()

        remaining_time += revolution_count_residual * Helper.get_time_for_one_ball_loop(avg_speed_last_rev)
        return remaining_time

    @staticmethod
    def find_zero(fun, a, b):
        """does not work very much with scipy and the 1D interpolation. That's why I wrote this."""
        b -= 1  # fix later.
        while b >= a:
            b -= 0.01
            if fun(b) > 0:
                return b

    @staticmethod
    def estimate_revolution_count_left_2(speeds_mean, index_start_of_speeds_mean, current_revolution, cutoff_speed):
        speeds_mean_fun = interp1d(range(len(speeds_mean)), speeds_mean - cutoff_speed)
        revolution_count_left = HelperConstantDeceleration.find_zero(speeds_mean_fun, a=0, b=len(speeds_mean))
        revolution_count_left -= (current_revolution + index_start_of_speeds_mean)
        if revolution_count_left < 0:
            raise PositiveValueExpectedException()
        return revolution_count_left

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

    @staticmethod
    def compute_model_2(diff_times, mean_speeds):
        speeds = np.apply_along_axis(func1d=Helper.get_ball_speed, axis=0, arr=diff_times)
        new_speeds = TimeSeriesMerger.find_index(speeds, mean_speeds)
        return np.where(new_speeds > 0)[0][0]
