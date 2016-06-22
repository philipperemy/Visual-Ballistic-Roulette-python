from __future__ import print_function

from Helper import *


class HelperConstantDeceleration(object):
    #  We should be able to average the deceleration factor. The intercept should not change.
    @staticmethod
    def estimate_time(constant_deceleration_model, current_revolution, cutoff_speed):
        revolution_count_left = HelperConstantDeceleration.estimate_revolution_count_left(constant_deceleration_model,
                                                                                          current_revolution,
                                                                                          cutoff_speed)
        revolution_count_floor = int(np.floor(revolution_count_left))
        remaining_time = 0.0
        i = 1
        while i <= revolution_count_floor:
            remaining_time += Helper.get_time_for_one_ball_loop(
                constant_deceleration_model.predict(current_revolution + i))
            i += 1
        revolution_count_residual = revolution_count_left - revolution_count_floor
        avg_speed_last_rev = 0.5 * constant_deceleration_model.predict(
            current_revolution + revolution_count_floor) + 0.5 * constant_deceleration_model.predict(
            current_revolution + revolution_count_floor + 1)
        remaining_time += revolution_count_residual * Helper.get_time_for_one_ball_loop(avg_speed_last_rev)
        return remaining_time

    @staticmethod
    def estimate_revolution_count_left(constant_deceleration_model, current_revolution, cutoff_speed):
        """ generated source for method estimate_revolutionCount_left """
        revolution_count_left = (cutoff_speed - constant_deceleration_model.get_intercept()) / \
                                constant_deceleration_model.get_slope() - current_revolution
        if revolution_count_left < 0:
            raise PositiveValueExpectedException()
        return revolution_count_left

    @staticmethod
    def compute_model(diff_times):
        speeds = []
        for diff_time in diff_times:
            speeds.append(Helper.get_ball_speed(diff_time))
        return Helper.perform_regression(range(1, len(speeds) + 1, 1), speeds)
