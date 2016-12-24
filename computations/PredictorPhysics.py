import numpy as np

from computations.Constants import Constants
from computations.Diamonds import Diamonds
from computations.Wheel import Wheel
from computations.utils.Helper import Helper
from computations.utils.Phase import Phase
from computations.utils.TimeSeriesMerger import TimeSeriesMerger
from utils.Exceptions import *
from utils.Logging import *


class PredictorPhysics(object):
    LAP_TIMES_ALL_GAMES = None

    @staticmethod
    def compute_inverse_for_games(ts_list):
        bs_list = []
        for ball_lap_times in ts_list:
            bs_list.append(np.apply_along_axis(func1d=Helper.get_inverse, axis=0, arr=ball_lap_times))
        mean_inverse_per_revolution = np.nanmean(TimeSeriesMerger.merge(bs_list), axis=0)
        return np.array(bs_list), mean_inverse_per_revolution

    @staticmethod
    def load_cache(database):
        """
        New convention is that the last ball lap times measure is done when the ball enters the diamonds ring.
        """
        lap_times_all_games = list()
        for session_id in database.get_session_ids():
            ball_recorded_times = database.select_ball_recorded_times(session_id)
            if len(ball_recorded_times) >= Constants.MIN_BALL_COUNT_OF_RECORDED_TIMES:
                ball_lap_times = Helper.compute_diff(Helper.convert_to_seconds(ball_recorded_times))
                lap_times_all_games.append(ball_lap_times)
        PredictorPhysics.LAP_TIMES_ALL_GAMES = np.array(lap_times_all_games)

    @staticmethod
    def predict_most_probable_number(ball_recorded_times, wheel_recorded_times, debug=False):

        if len(wheel_recorded_times) < Constants.MIN_WHEEL_COUNT_OF_RECORDED_TIMES:
            raise SessionNotReadyException()

        if len(ball_recorded_times) < Constants.MIN_BALL_COUNT_OF_RECORDED_TIMES:
            raise SessionNotReadyException()

        ball_recorded_times = Helper.convert_to_seconds(ball_recorded_times)
        wheel_recorded_times = Helper.convert_to_seconds(wheel_recorded_times)

        most_probable_number = PredictorPhysics.predict(ball_recorded_times,
                                                        wheel_recorded_times,
                                                        debug)
        return most_probable_number

    @staticmethod
    def predict(ball_recorded_times, wheel_recorded_times, debug):
        ts_list = PredictorPhysics.LAP_TIMES_ALL_GAMES

        if ts_list is None:
            raise CriticalException('Cache is not initialized. Call load_cache().')

        # inverse_ts_list, inverse_ts_mean = PredictorPhysics.compute_inverse_for_games(ts_list)
        ts_mean = np.nanmean(TimeSeriesMerger.merge(ts_list), axis=0)

        last_time_ball_passes_in_front_of_ref = ball_recorded_times[-1]
        last_wheel_lap_time_in_front_of_ref = Helper.get_last_time_wheel_is_in_front_of_ref(wheel_recorded_times,
                                                                                            last_time_ball_passes_in_front_of_ref)
        log('reference time of prediction = {} s'.format(last_time_ball_passes_in_front_of_ref), debug)
        ball_lap_times = Helper.compute_diff(ball_recorded_times)
        wheel_lap_times = Helper.compute_diff(wheel_recorded_times)
        ball_loop_count = len(ball_lap_times)

        # can probably match with the lap times. We de-couple the hyper parameters.
        # maybe inverse is less sensitive to error measurements.
        # inverse_lap_times = np.apply_along_axis(func1d=Helper.get_inverse, axis=0, arr=ball_lap_times)

        # check all indices
        index_of_rev_start = Helper.find_abs_start_index(ball_lap_times, ts_mean)
        index_of_last_recorded_time = ball_loop_count + index_of_rev_start

        matched_game_indices = TimeSeriesMerger.find_nearest_neighbors(ball_lap_times,
                                                                       ts_list,
                                                                       index_of_rev_start,
                                                                       neighbors_count=Constants.NEAREST_NEIGHBORS_COUNT)
        # average across all the neighbors residuals
        estimated_time_left = np.mean(np.sum(ts_list[matched_game_indices, index_of_last_recorded_time:], axis=1))

        # TODO: very simple way to calculate it. Might be more complex.
        increasing_factor = np.mean(ts_list[matched_game_indices, 1:] / ts_list[matched_game_indices, :-1])

        # if we have [0, 0, 1, 2, 3, 0, 0], index_of_rev_start = 2, index_current_abs = 2 + 3 - 1 = 4
        # because the last loop is not complete so -1 (due to new convention).
        rem_loops = ts_list[matched_game_indices, index_of_last_recorded_time:].shape[1] - 1
        # check if * or /
        rem_res_loop = np.mean(
            ts_list[matched_game_indices, -1] / ts_list[matched_game_indices, -2]) / increasing_factor
        number_of_revolutions_left_ball = rem_loops + rem_res_loop

        if number_of_revolutions_left_ball <= 0:
            error_msg = 'rem_loops = {}, rem_res_loop = {}.'.format(rem_loops, rem_res_loop)
            raise PositiveValueExpectedException('number_of_revolutions_left_ball should be positive. ' + error_msg)

        log('number_of_revolutions_left_ball = {}'.format(number_of_revolutions_left_ball))
        log('estimated_time_left = {}'.format(estimated_time_left))
        log('________________________________')

        # the time values are always taken at the same diamond.
        diamond = Diamonds.detect_diamonds(number_of_revolutions_left_ball)
        log('diamond to be hit = {}'.format(diamond))

        if diamond == Diamonds.DiamondType.BLOCKER:
            expected_bouncing_shift = Constants.EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND
        else:
            expected_bouncing_shift = Constants.EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND

        shift_ball_cutoff = (number_of_revolutions_left_ball % 1) * len(Wheel.NUMBERS)
        time_at_cutoff_ball = last_time_ball_passes_in_front_of_ref + estimated_time_left

        if time_at_cutoff_ball < last_time_ball_passes_in_front_of_ref + Constants.SECONDS_NEEDED_TO_PLACE_BETS:
            raise PositiveValueExpectedException()

        wheel_last_revolution_time = wheel_lap_times[-1]
        initial_number = Phase.find_phase_number_between_ball_and_wheel(last_time_ball_passes_in_front_of_ref,
                                                                        last_wheel_lap_time_in_front_of_ref,
                                                                        wheel_last_revolution_time,
                                                                        Constants.DEFAULT_WHEEL_WAY)

        # check how it is computed in details. Can't make up my mind now.
        shift_between_initial_time_and_cutoff = ((estimated_time_left / wheel_last_revolution_time) % 1) * len(
            Wheel.NUMBERS)

        shift_to_add = shift_ball_cutoff + shift_between_initial_time_and_cutoff
        predicted_number_cutoff = Wheel.get_number_with_shift(initial_number, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
        log("shift_between_initial_time_and_cutoff = {}".format(shift_between_initial_time_and_cutoff), debug)
        log("predicted_number_cutoff is = {}".format(predicted_number_cutoff), debug)

        log("expected_bouncing_shift = {}".format(expected_bouncing_shift), debug)
        shift_to_add += expected_bouncing_shift
        predicted_number = Wheel.get_number_with_shift(initial_number, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
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

        # HYPER PARAMETER RELATION WITH QUANTITIES
        # - estimated_time_left (NOTHING) BALL SPEED IS NOT NEEDED.
        # - number_of_revolutions_left_ball (NOTHING) BALL SPEED IS NOT NEEDED.
        # - PHASE 2 - if both quantities are correct, we can estimate predicted_number_cutoff exactly (without any
        # errors on the measurements).
        # - initial_number (NOTHING) WHEEL SPEED IS NOT NEEDED.
        # - predicted_number_cutoff
        # - predicted_number (less important)
        # - diamond: FORWARD, BLOCKER, NO_DIAMOND (position of the diamond)

        #     # constants to optimise.
        #   EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND = 16
        #   EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND = 6
        #   MOVE_TO_NEXT_DIAMOND = 0  # due to the intrinsic speed. might change something. to be removed maybe later.
        #
        # Important
        # Actually we don't need BALL_SPEED, WHEEL_SPEED, CUTOFF_SPEED !
        return predicted_number
