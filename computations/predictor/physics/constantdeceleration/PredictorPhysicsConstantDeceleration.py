from HelperConstantDeceleration import *
from computations.predictor.Phase import *
from utils.Logging import *


class PredictorPhysicsConstantDeceleration(object):
    @staticmethod
    def predict_most_probable_number(ball_cumsum_times, wheel_cumsum_times, debug=False):

        if len(wheel_cumsum_times) < Constants.MIN_NUMBER_OF_WHEEL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        if len(ball_cumsum_times) < Constants.MIN_NUMBER_OF_BALL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        # in seconds.
        ball_cumsum_times = np.array(Helper.convert_to_seconds(ball_cumsum_times))
        wheel_cumsum_times = np.array(Helper.convert_to_seconds(wheel_cumsum_times))

        most_probable_number = PredictorPhysicsConstantDeceleration.predict(ball_cumsum_times, wheel_cumsum_times,
                                                                            debug)
        return most_probable_number

    @staticmethod
    def predict(ball_cumsum_times, wheel_cumsum_times, debug):
        cutoff_speed = Constants.CUTOFF_SPEED
        origin_time_ball = ball_cumsum_times[0]
        """Think about merging all together and having the same time index."""
        last_wheel_lap_time_in_front_of_ref = Helper.get_last_time_wheel_is_in_front_of_ref(wheel_cumsum_times,
                                                                                            ball_cumsum_times[-1])
        ball_cumsum_times = Helper.normalize(ball_cumsum_times, origin_time_ball)
        origin_time_wheel = wheel_cumsum_times[0]
        wheel_cumsum_times = Helper.normalize(wheel_cumsum_times, origin_time_wheel)
        diff_origin = origin_time_ball - origin_time_wheel
        last_time_ball_passes_in_front_of_ref = ball_cumsum_times[-1]
        last_wheel_lap_time_in_front_of_ref -= origin_time_wheel
        log('Reference time of prediction = {} s'.format(last_time_ball_passes_in_front_of_ref), debug)
        ball_diff_times = Helper.compute_diff(ball_cumsum_times)
        wheel_diff_times = Helper.compute_diff(wheel_cumsum_times)
        ball_model = HelperConstantDeceleration.compute_model(ball_diff_times)
        number_of_revolutions_left_ball = HelperConstantDeceleration.estimate_revolution_count_left(ball_model, len(
            ball_diff_times), cutoff_speed)
        phase_at_cut_off = (number_of_revolutions_left_ball % 1) * len(Wheel.NUMBERS)

        estimated_time_left = HelperConstantDeceleration.estimate_time(ball_model, len(ball_diff_times),
                                                                       number_of_revolutions_left_ball)
        time_at_cutoff_ball = last_time_ball_passes_in_front_of_ref + estimated_time_left

        if time_at_cutoff_ball < last_time_ball_passes_in_front_of_ref + Constants.TIME_LEFT_FOR_PLACING_BETS_SECONDS:
            raise PositiveValueExpectedException()

        constant_wheel_speed = Helper.get_wheel_speed(wheel_diff_times[-1])
        wheel_speed_in_front_of_mark = constant_wheel_speed
        last_known_speed_wheel = constant_wheel_speed
        initial_phase = Phase.find_phase_number_between_ball_and_wheel(last_time_ball_passes_in_front_of_ref,
                                                                       last_wheel_lap_time_in_front_of_ref - diff_origin,
                                                                       wheel_speed_in_front_of_mark,
                                                                       Constants.DEFAULT_WHEEL_WAY)

        shift_phase_between_initial_time_and_cutoff = ((estimated_time_left / wheel_diff_times[-1]) % 1) * len(
            Wheel.NUMBERS)

        adjusted_initial_phase = (Constants.DEFAULT_SHIFT_PHASE * last_known_speed_wheel)
        final_phase_to_add = shift_phase_between_initial_time_and_cutoff + phase_at_cut_off + adjusted_initial_phase
        final_phase_to_add = int(np.round(final_phase_to_add))

        predicted_number = Wheel.get_number_with_phase(initial_phase, final_phase_to_add, Constants.DEFAULT_WHEEL_WAY)

        log("Number of pockets (computed from angle) = {}".format(shift_phase_between_initial_time_and_cutoff), debug)
        log("adjusted_initial_phase = {}".format(adjusted_initial_phase), debug)
        log("predicted_number is = {}".format(predicted_number), debug)
        return predicted_number
