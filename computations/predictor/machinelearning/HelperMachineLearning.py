from computations.predictor.Phase import *
from utils.Logging import *


class HelperMachineLearning(object):
    # code not used.
    @staticmethod
    def build_data_records(ball_cumsum_times, wheel_cumsum_times):
        data_records = list()
        if len(ball_cumsum_times) == 0 or len(wheel_cumsum_times) == 0:
            return data_records

        # no more normalisation like this.
        origin_time_ball = ball_cumsum_times[0]
        ball_cumsum_times = Helper.normalize(ball_cumsum_times, origin_time_ball)

        origin_time_wheel = wheel_cumsum_times[0]
        wheel_cumsum_times = Helper.normalize(wheel_cumsum_times, origin_time_wheel)

        diff_origin = origin_time_ball - origin_time_wheel

        ball_diff_times = Helper.compute_diff(ball_cumsum_times)
        range_ball = range(1, len(ball_diff_times) + 1)

        # not used. TODO bug.
        ball_speed_model = Helper.perform_regression(range_ball, ball_diff_times)

        wheel_diff_times = Helper.compute_diff(wheel_cumsum_times)
        constant_wheel_speed = Helper.get_wheel_speed(wheel_diff_times[-1])

        for i in range(len(ball_cumsum_times)):
            corresponding_ball_lap_time = ball_cumsum_times[i]
            wheel_speed_in_front_of_mark = constant_wheel_speed

            last_wheel_lap_time_in_front_ref = Helper.get_last_time_wheel_is_in_front_of_ref(wheel_cumsum_times,
                                                                                             corresponding_ball_lap_time + diff_origin)
            if last_wheel_lap_time_in_front_ref is None:
                log('Ball time = {} is ahead of the wheel. Skipping.'.format(corresponding_ball_lap_time))
                continue

            phase = Phase.find_phase_number_between_ball_and_wheel(corresponding_ball_lap_time,
                                                                   last_wheel_lap_time_in_front_ref,
                                                                   wheel_speed_in_front_of_mark,
                                                                   Constants.DEFAULT_WHEEL_WAY)
            record = dict()
            record['ball_speed_in_front_of_mark'] = 0  # TODO change it.
            record['wheel_speed_in_front_of_mark'] = wheel_speed_in_front_of_mark
            record['phase_of_wheel_when_ball_passes_in_front_of_mark'] = phase
            data_records.append(record)
        return data_records
