#!/usr/bin/env python
""" generated source for module Predictor_physicsConstant_deceleration """
from __future__ import print_function

import PredictorPhysics
from HelperConstantDeceleration import *


class PredictorPhysicsConstantDeceleration(PredictorPhysics):

    def predict(self, ball_cumsum_times, wheel_cumsum_times):
        cutoff_speed = Constants.CUTOFF_SPEED
        origin_time_ball = Helper.head(ball_cumsum_times)
        ball_cumsum_times = Helper.normalize(ball_cumsum_times, origin_time_ball)
        origin_time_wheel = Helper.head(wheel_cumsum_times)
        wheel_cumsum_times = Helper.normalize(wheel_cumsum_times, origin_time_wheel)
        diff_origin = origin_time_ball - origin_time_wheel
        last_time_ball_passes_in_front_of_ref = Helper.peek(ball_cumsum_times)
        print("Reference time of prediction = " + str(last_time_ball_passes_in_front_of_ref) + " s")
        ball_diff_times = Helper.compute_diff(ball_cumsum_times)
        wheel_diff_times = Helper.compute_diff(wheel_cumsum_times)
        ball_model = HelperConstantDeceleration.compute_model(ball_diff_times)
        number_of_revolutions_left_ball = HelperConstantDeceleration.estimate_revolution_count_left(ball_model,
                                                                                                    len(
                                                                                                        ball_diff_times),
                                                                                                    cutoff_speed)
        phase_at_cut_off = int((number_of_revolutions_left_ball % 1) * Wheel.NUMBERS.length)
        time_at_cutoff_ball = last_time_ball_passes_in_front_of_ref + \
                              HelperConstantDeceleration.estimate_time(ball_model, len(ball_diff_times), cutoff_speed)
        return super(self.__class__, self).predict(wheel_cumsum_times, diff_origin,
                                                   last_time_ball_passes_in_front_of_ref,
                                                   wheel_diff_times,
                                                   phase_at_cut_off, time_at_cutoff_ball)