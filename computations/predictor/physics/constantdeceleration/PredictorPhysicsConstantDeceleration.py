#!/usr/bin/env python
""" generated source for module Predictor_physicsConstant_deceleration """
from __future__ import print_function

from HelperConstantDeceleration import *


class PredictorPhysicsConstantDeceleration(object):
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
        if time_at_cutoff_ball < last_time_ball_passes_in_front_of_ref + Constants.TIME_LEFT_FOR_PLACING_BETS_SECONDS:
            raise PositiveValueExpectedException()

        last_wheel_lap_time_in_front_of_ref = Helper.get_last_time_wheel_is_in_front_of_ref(wheel_cumsum_times,
                                                                                            last_time_ball_passes_in_front_of_ref)
        constant_wheel_speed = Helper.get_wheel_speed(wheel_diff_times[-1])
        wheel_speed_in_front_of_mark = constant_wheel_speed
        last_known_speed_wheel = constant_wheel_speed
        initial_phase = Phase.find_phase_number_between_ball_and_wheel(last_time_ball_passes_in_front_of_ref,
                                                                       last_wheel_lap_time_in_front_of_ref - diff_origin,
                                                                       wheel_speed_in_front_of_mark,
                                                                       Constants.DEFAULT_WHEEL_WAY)
        shift_phase_between_initial_time_and_cut_off = int(
            ((time_at_cutoff_ball - last_time_ball_passes_in_front_of_ref) /
             wheel_diff_times[-1] % 1) * Wheel.NUMBERS.length)

        number_below_ball_at_cutoff = Wheel.get_number_with_phase(initial_phase,
                                                                  shift_phase_between_initial_time_and_cut_off +
                                                                  phase_at_cut_off,
                                                                  Constants.DEFAULT_WHEEL_WAY)
        adjusted_initial_phase = int((Constants.DEFAULT_SHIFT_PHASE * last_known_speed_wheel))
        print("Number of pockets (computed from angle) = " + str(shift_phase_between_initial_time_and_cut_off))
        print("DEFAULT_SHIFT_PHASE = " + str(adjusted_initial_phase))
        predicted_number = Wheel.get_number_with_phase(number_below_ball_at_cutoff, adjusted_initial_phase,
                                                       Constants.DEFAULT_WHEEL_WAY)
        print("Predicted number is = " + predicted_number)
        return predicted_number
