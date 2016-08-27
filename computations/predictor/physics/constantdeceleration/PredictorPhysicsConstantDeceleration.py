from HelperConstantDeceleration import *
from TimeSeriesMerger import *
from computations.predictor.Phase import *
from utils.Logging import *


class PredictorPhysicsConstantDeceleration(object):
    FIXED_SLOPE = None
    MEAN_SPEED_PER_REVOLUTION = None

    @staticmethod
    def load_cache(database):
        slopes = []
        bs_list = list()
        for session_id in database.get_session_ids():
            ball_cum_sum_times = database.select_ball_lap_times(session_id)
            if len(ball_cum_sum_times) >= Constants.MIN_NUMBER_OF_BALL_TIMES_BEFORE_PREDICTION:
                ball_cum_sum_times = Helper.convert_to_seconds(ball_cum_sum_times)
                ball_diff_times = Helper.compute_diff(ball_cum_sum_times)

                regress = ball_diff_times[-3:]  # to change. the end seems linear.
                ball_model = HelperConstantDeceleration.compute_model(regress)
                slopes.append(ball_model.coef_[0, 0])

                # import matplotlib.pyplot as plt
                # plt.plot(ball_diff_times)
                # plt.show()

                bs_list.append(np.apply_along_axis(func1d=Helper.get_ball_speed, axis=0, arr=ball_diff_times))
        log('Slopes = {}'.format(Helper.round_digits(slopes)))
        mean_slopes = np.mean(slopes)
        log('Mean(Slopes) = {}'.format(mean_slopes))

        mean_speed_per_revolution = np.nanmean(TimeSeriesMerger.merge(bs_list), axis=0)
        # plt.plot(mean_speed_per_revolution)
        PredictorPhysicsConstantDeceleration.FIXED_SLOPE = mean_slopes
        PredictorPhysicsConstantDeceleration.MEAN_SPEED_PER_REVOLUTION = mean_speed_per_revolution

    @staticmethod
    def predict_most_probable_number(ball_cum_sum_times, wheel_cum_sum_times, debug=False):

        if len(wheel_cum_sum_times) < Constants.MIN_NUMBER_OF_WHEEL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        if len(ball_cum_sum_times) < Constants.MIN_NUMBER_OF_BALL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        ball_cum_sum_times = Helper.convert_to_seconds(ball_cum_sum_times)
        wheel_cum_sum_times = Helper.convert_to_seconds(wheel_cum_sum_times)

        most_probable_number = PredictorPhysicsConstantDeceleration.predict(ball_cum_sum_times,
                                                                            wheel_cum_sum_times,
                                                                            debug)
        return most_probable_number

    @staticmethod
    def predict(ball_cum_sum_times, wheel_cum_sum_times, debug):
        cutoff_speed = Constants.CUTOFF_SPEED
        speeds_mean = PredictorPhysicsConstantDeceleration.MEAN_SPEED_PER_REVOLUTION

        last_time_ball_passes_in_front_of_ref = ball_cum_sum_times[-1]
        last_wheel_lap_time_in_front_of_ref = Helper.get_last_time_wheel_is_in_front_of_ref(wheel_cum_sum_times,
                                                                                            last_time_ball_passes_in_front_of_ref)

        log('Reference time of prediction = {} s'.format(last_time_ball_passes_in_front_of_ref), debug)
        ball_diff_times = Helper.compute_diff(ball_cum_sum_times)
        wheel_diff_times = Helper.compute_diff(wheel_cum_sum_times)
        ball_loop_count = len(ball_diff_times)

        # check all indices
        index_of_rev_start = HelperConstantDeceleration.compute_model_2(ball_diff_times, speeds_mean)

        # if we have [0, 0, 1, 2, 3, 0, 0], index_of_rev_start = 2, index_current_abs = 2 + 3 - 1 = 4
        index_of_last_known_speed = ball_loop_count + index_of_rev_start - 1
        number_of_revolutions_left_ball = HelperConstantDeceleration.estimate_revolution_count_left_2(speeds_mean,
                                                                                                      index_of_last_known_speed,
                                                                                                      cutoff_speed)
        estimated_time_left = HelperConstantDeceleration.estimate_time_2(speeds_mean,
                                                                         index_of_last_known_speed,
                                                                         number_of_revolutions_left_ball)

        log('number_of_revolutions_left_ball = {}'.format(number_of_revolutions_left_ball))
        log('estimated_time_left = {}'.format(estimated_time_left))
        log('________________________________')

        diamond = HelperConstantDeceleration.detect_diamonds(number_of_revolutions_left_ball)
        log('Diamond to be hit = {}'.format(diamond))

        if diamond == Constants.DiamondType.BLOCKER:
            expected_bouncing_shift = 6
        else:
            expected_bouncing_shift = 16

        shift_ball_cutoff = (number_of_revolutions_left_ball % 1) * len(Wheel.NUMBERS)
        time_at_cutoff_ball = last_time_ball_passes_in_front_of_ref + estimated_time_left

        if time_at_cutoff_ball < last_time_ball_passes_in_front_of_ref + Constants.SECONDS_NEEDED_TO_PLACE_BETS:
            raise PositiveValueExpectedException()

        constant_wheel_speed = Helper.get_wheel_speed(wheel_diff_times[-1])
        initial_phase = Phase.find_phase_number_between_ball_and_wheel(last_time_ball_passes_in_front_of_ref,
                                                                       last_wheel_lap_time_in_front_of_ref,
                                                                       constant_wheel_speed,
                                                                       Constants.DEFAULT_WHEEL_WAY)

        shift_between_initial_time_and_cutoff = ((estimated_time_left / wheel_diff_times[-1]) % 1) * len(
            Wheel.NUMBERS)

        shift_to_add = shift_ball_cutoff + shift_between_initial_time_and_cutoff
        predicted_number_cutoff = Wheel.get_number_with_phase(initial_phase, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
        log("shift_between_initial_time_and_cutoff = {}".format(shift_between_initial_time_and_cutoff), debug)
        log("predicted_number_cutoff is = {}".format(predicted_number_cutoff), debug)

        log("expected_bouncing_shift = {}".format(expected_bouncing_shift), debug)
        shift_to_add += expected_bouncing_shift
        predicted_number = Wheel.get_number_with_phase(initial_phase, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
        log("predicted_number is = {}".format(predicted_number), debug)

        # possibility to assess the error on:
        # - PHASE 1
        # - number_of_revolutions_left_ball
        # - estimated_time_left
        # - PHASE 2 - if both quantities are correct, we can estimate predicted_number_cutoff exactly (without any
        # errors on the measurements).
        # - predicted_number_cutoff
        # - predicted_number (less important)
        # - diamond: FORWARD, BLOCKER, NO_DIAMOND (position of the diamond)
        return predicted_number
