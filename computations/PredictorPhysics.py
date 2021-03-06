import numpy as np

from computations.Constants import Constants
from computations.Diamonds import Diamonds
from computations.Wheel import Wheel
from computations.comp_utils.Helper import Helper
from computations.comp_utils.Phase import Phase
from computations.comp_utils.TimeSeriesMerger import TimeSeriesMerger
from utils.Exceptions import *
from utils.Logging import *


class PredictorPhysics(object):
    LAP_TIMES_ALL_GAMES_LIST = None  # contains all the lap times for the known games
    DIAMOND_RING_ALL_GAMES_LIST = None  # contains all the times between the last landmark 0 and the diamond rings

    @staticmethod
    def compute_inverse_for_games(ts_list):
        bs_list = []
        for ball_lap_times in ts_list:
            bs_list.append(1.0 / np.array(ball_lap_times))
        mean_inverse_per_revolution = np.nanmean(TimeSeriesMerger.merge(bs_list), axis=0)
        return np.array(bs_list), mean_inverse_per_revolution

    @staticmethod
    def load_cache(database):
        # at least not when we compare the values for the mean to find abs_rev_start
        lap_times_all_games_list = list()
        diamond_ring_all_games_list = list()
        for session_id in database.get_session_ids():
            ball_recorded_times = database.select_ball_recorded_times(session_id)
            if len(ball_recorded_times) >= Constants.MIN_BALL_COUNT_OF_RECORDED_TIMES:
                ball_lap_times = np.diff(Helper.convert_to_seconds(ball_recorded_times))
                lap_times_all_games_list.append(ball_lap_times[:-1])
                diamond_ring_all_games_list.append(ball_lap_times[-1])
        PredictorPhysics.LAP_TIMES_ALL_GAMES_LIST = lap_times_all_games_list
        PredictorPhysics.DIAMOND_RING_ALL_GAMES_LIST = diamond_ring_all_games_list

    @staticmethod
    def predict_most_probable_number(ball_recorded_times, wheel_recorded_times, debug=False):

        if len(wheel_recorded_times) < Constants.MIN_WHEEL_COUNT_OF_RECORDED_TIMES:
            raise SessionNotReadyException('Session not ready. Too few wheel recorded times.')

        if len(ball_recorded_times) < Constants.MIN_BALL_COUNT_OF_RECORDED_TIMES:
            raise SessionNotReadyException('Session not ready. Too few ball recorded times.')

        ball_recorded_times = Helper.convert_to_seconds(ball_recorded_times)
        wheel_recorded_times = Helper.convert_to_seconds(wheel_recorded_times)

        most_probable_number_cutoff, most_probable_number = PredictorPhysics.predict(ball_recorded_times,
                                                                                     wheel_recorded_times,
                                                                                     debug)
        return most_probable_number_cutoff, most_probable_number

    @staticmethod
    def predict(ball_recorded_times, wheel_recorded_times, debug=True):
        # Last measurement is when the ball hits the diamond ring.
        ts_list = np.array(PredictorPhysics.LAP_TIMES_ALL_GAMES_LIST.copy())
        dr_list = np.array(PredictorPhysics.DIAMOND_RING_ALL_GAMES_LIST.copy())

        if ts_list is None or dr_list is None:
            raise CriticalException('Cache is not initialized. Call load_cache().')

        ts_list = TimeSeriesMerger.merge(ts_list)
        ts_mean = np.nanmean(ts_list, axis=0)

        last_time_ball_passes_in_front_of_ref = ball_recorded_times[-1]
        last_wheel_lap_time_in_front_of_ref = Helper.get_last_time_wheel_is_in_front_of_ref(
            wheel_recorded_times, last_time_ball_passes_in_front_of_ref)
        log('ref time of the prediction = {0:.2f}s'.format(last_time_ball_passes_in_front_of_ref), debug)
        ball_lap_times = np.diff(ball_recorded_times)
        wheel_lap_times = np.diff(wheel_recorded_times)
        ball_loop_count = len(ball_lap_times)

        index_of_rev_start = Helper.find_abs_start_index(ball_lap_times, ts_mean)
        log('index_of_rev_start = {}'.format(index_of_rev_start), debug)
        index_of_last_recorded_time = ball_loop_count + index_of_rev_start

        matched_game_indices = TimeSeriesMerger.find_nearest_neighbors(ball_lap_times,
                                                                       ts_list,
                                                                       index_of_rev_start,
                                                                       neighbors_count=Constants.NEAREST_NEIGHBORS_COUNT)
        log('matched_game_indices = {}'.format(matched_game_indices), debug)

        estimated_time_left = np.mean(np.sum(ts_list[matched_game_indices, index_of_last_recorded_time:], axis=1))
        estimated_time_left += np.mean(dr_list[matched_game_indices], axis=0)
        log('estimated_time_left = {0:.2f}s'.format(estimated_time_left), debug)

        if estimated_time_left <= 0:
            raise PositiveValueExpectedException('estimated_time_left must be positive.')

        # biased estimator but still it should work here.
        max_residual_time = np.max(dr_list)

        # if we have [0, 0, 1, 2, 3, 0, 0], index_of_rev_start = 2
        # rem_loops is actually useless to compute :)
        rem_loops = ts_list[matched_game_indices, index_of_last_recorded_time:].shape[1]

        rem_res_loop = np.mean(dr_list[matched_game_indices] / max_residual_time)  # we should calibrate it more.
        number_of_revolutions_left_ball = rem_loops + rem_res_loop

        # TODO: for later.
        # we need to have a better approximation of:
        # We can maybe fit an ARIMA on the Abs Ball times
        # or get rem_res_loop accurate.

        if number_of_revolutions_left_ball <= 0:
            error_msg = 'rem_loops = {0:.2f}, rem_res_loop = {0:.2f}.'.format(rem_loops, rem_res_loop)
            raise PositiveValueExpectedException('number_of_revolutions_left_ball must be positive.' + error_msg)

        log('number_of_revolutions_left_ball = {0:.2f}'.format(number_of_revolutions_left_ball), debug)

        # the time values are always taken at the same diamond.
        diamond = Diamonds.detect_diamonds(number_of_revolutions_left_ball)
        log('diamond to be hit = {}'.format(diamond), debug)

        if diamond == Diamonds.DiamondType.BLOCKER:
            expected_bouncing_shift = Constants.EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND
        else:
            expected_bouncing_shift = Constants.EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND

        shift_ball_cutoff = (number_of_revolutions_left_ball % 1) * len(Wheel.NUMBERS)
        time_at_cutoff_ball = last_time_ball_passes_in_front_of_ref + estimated_time_left

        if time_at_cutoff_ball < last_time_ball_passes_in_front_of_ref + Constants.SECONDS_NEEDED_TO_PLACE_BETS:
            raise PositiveValueExpectedException()

        wheel_last_revolution_time = wheel_lap_times[-1]
        # We want to find the number of the wheel where the ball passes in front of the mark.
        initial_number = Phase.find_phase_number_between_ball_and_wheel(last_time_ball_passes_in_front_of_ref,
                                                                        last_wheel_lap_time_in_front_of_ref,
                                                                        wheel_last_revolution_time,
                                                                        Constants.DEFAULT_WHEEL_WAY)

        shift_between_initial_time_and_cutoff = ((estimated_time_left / wheel_last_revolution_time) % 1) * len(
            Wheel.NUMBERS)

        # Explanation:
        # shift_between_initial_time_and_cutoff - let's not focus on the ball. What is the configuration of the wheel
        # at the cutoff time, i.e. estimated_time_left seconds later.
        # shift_ball_cutoff - the ball is also moving during this time. Let's not focus on the wheel. Where is the ball
        # compared to the wheel at the cutoff time. We imagine that the wheel is fixed.
        # We then add the two quantities (composition of the kinetics) to know about the real shift.
        shift_to_add = shift_ball_cutoff + shift_between_initial_time_and_cutoff
        predicted_number_cutoff = Wheel.get_number_with_shift(initial_number, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
        log('shift_between_initial_time_and_cutoff = {0:.2f}'.format(shift_between_initial_time_and_cutoff), debug)
        log('shift_ball_cutoff = {0:.2f}'.format(shift_ball_cutoff), debug)
        log('predicted_number_cutoff = {}'.format(predicted_number_cutoff), debug)
        log('expected_bouncing_shift = {}'.format(expected_bouncing_shift), debug)
        shift_to_add += expected_bouncing_shift
        predicted_number = Wheel.get_number_with_shift(initial_number, shift_to_add, Constants.DEFAULT_WHEEL_WAY)
        log('predicted_number is = {}'.format(predicted_number), debug)
        return predicted_number_cutoff, predicted_number

        # Equal to predicted_number_cutoff
        # Phase.find_phase_number_between_ball_and_wheel(time_at_cutoff_ball,
        #                                        last_wheel_lap_time_in_front_of_ref,
        #                                        wheel_last_revolution_time,
        #                                        Constants.DEFAULT_WHEEL_WAY)
