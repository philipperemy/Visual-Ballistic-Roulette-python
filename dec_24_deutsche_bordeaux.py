from computations.PredictorPhysics import *
from computations.comp_utils.Measures import *
from database.DatabaseAccessor import *
from read_results import read_experimentation_results, assert_equals


def run(bounce_blocker, bounce_forward):
    Constants.EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND = bounce_blocker
    Constants.EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND = bounce_forward
    failures = 0.0
    expected_numbers = []
    predicted_numbers = []
    deterministic_expected_numbers = []
    deterministic_predicted_numbers = []
    for predicted in predictions:
        session_id = predicted['video_id']
        BS = np.array(da.select_ball_recorded_times(session_id))
        WS = np.array(da.select_wheel_recorded_times(session_id))
        try:
            for depth in range(1, 2):
                new_BS = BS[:-depth]
                new_WS = WS[WS < max(new_BS)]  # must be measurable.
                det_number, number = PredictorPhysics.predict_most_probable_number(new_BS, new_WS, debug=False)
                det_error = AngularMeasure(det_number, da.get_deterministic_outcome(session_id)).error()
                # print('ses_id = {}, det_error = {}, depth = {}'.format(session_id, det_error, depth))
                expected_numbers.append(da.get_outcome(session_id))
                predicted_numbers.append(number)
                deterministic_expected_numbers.append(da.get_deterministic_outcome(session_id))
                deterministic_predicted_numbers.append(det_number)
        except:
            print('ses_id = {}, FAILURE'.format(session_id))
            failures += 1.0

    final_errors = []
    for (e, p) in zip(expected_numbers, predicted_numbers):
        final_errors.append(AngularMeasure(e, p).error())

    det_errors = []
    for (e, p) in zip(deterministic_expected_numbers, deterministic_predicted_numbers):
        det_errors.append(AngularMeasure(e, p).error())

    print('mean =', np.mean(final_errors), 'final_errors =', final_errors)
    print('mean =', np.mean(det_errors), 'det_errors =', det_errors)
    print('total failures = {}'.format(float(failures) / len(predictions)))
    return np.mean(final_errors)


if __name__ == '__main__':
    try:
        os.remove('roulette-experiment.db')
    except:
        pass

    da = DatabaseAccessor.get_instance()

    predictions = read_experimentation_results()

    for predicted in predictions:
        new_session_id = da.increment_and_get_session_id()
        print(new_session_id)
        assert_equals(str(new_session_id), predicted['video_id'])
        for bs in np.array(predicted['ball_lap_times']) * 1000:
            da.insert_ball_lap_times(new_session_id, float(bs))
        for ws in np.array(predicted['wheel_lap_times']) * 1000:
            da.insert_wheel_lap_times(new_session_id, float(ws))

    # add last value when the ball hits the diamond.
    da.insert_ball_lap_times(1, 15.616 * 1000)
    da.insert_ball_lap_times(2, 11.949 * 1000)
    da.insert_ball_lap_times(3, 13.033 * 1000)
    da.insert_ball_lap_times(4, 17.783 * 1000)
    da.insert_ball_lap_times(5, 18.749 * 1000)
    da.insert_ball_lap_times(6, 18.349 * 1000)
    da.insert_ball_lap_times(7, 18.233 * 1000)
    da.insert_ball_lap_times(8, 16.700 * 1000)
    da.insert_ball_lap_times(9, 21.749 * 1000)
    da.insert_ball_lap_times(10, 21.116 * 1000)
    da.insert_ball_lap_times(11, 16.333 * 1000)
    da.insert_ball_lap_times(12, 14.733 * 1000)
    da.insert_ball_lap_times(13, 17.716 * 1000)
    da.insert_ball_lap_times(14, 18.233 * 1000)
    da.insert_ball_lap_times(15, 18.733 * 1000)
    da.insert_ball_lap_times(16, 18.466 * 1000)
    da.insert_ball_lap_times(17, 15.300 * 1000)
    da.insert_ball_lap_times(18, 19.800 * 1000)
    da.insert_ball_lap_times(19, 22.600 * 1000)
    da.insert_ball_lap_times(20, 20.333 * 1000)
    da.insert_ball_lap_times(21, 15.016 * 1000)
    da.insert_ball_lap_times(22, 18.333 * 1000)
    da.insert_ball_lap_times(23, 19.233 * 1000)
    da.insert_ball_lap_times(24, 20.249 * 1000)
    da.insert_ball_lap_times(25, 18.533 * 1000)
    da.insert_ball_lap_times(26, 18.283 * 1000)
    da.insert_ball_lap_times(27, 16.849 * 1000)

    da.insert_outcome(1, 29, 15)
    da.insert_outcome(2, 2, 24)
    da.insert_outcome(3, 22, 23)
    da.insert_outcome(4, 13, 20)
    da.insert_outcome(5, 15, 10)
    da.insert_outcome(6, 32, 33)
    da.insert_outcome(7, 31, 19)
    da.insert_outcome(8, 16, 5)
    da.insert_outcome(9, 15, 33)
    da.insert_outcome(10, 14, 12)
    da.insert_outcome(11, 27, 26)
    da.insert_outcome(12, 23, 33)
    da.insert_outcome(13, 9, 36)
    da.insert_outcome(14, 24, 11)
    da.insert_outcome(15, 34, 35)
    da.insert_outcome(16, 20, 8)
    da.insert_outcome(17, 14, 30)
    da.insert_outcome(18, 32, 24)
    da.insert_outcome(19, 8, 33)
    da.insert_outcome(20, 11, 14)
    da.insert_outcome(21, 6, 20)
    da.insert_outcome(22, 15, 31)
    da.insert_outcome(23, 0, 25)
    da.insert_outcome(24, 14, 31)
    da.insert_outcome(25, 29, 5)
    da.insert_outcome(26, 22, 26)
    da.insert_outcome(27, 0, 34)

    PredictorPhysics.load_cache(da)

    run(22, 30)
    # err = []
    # for i in range(37):
    #    for j in range(37):
    #        err.append((i, j, run(i, j)))
    #        print(i, j)
    # print(err)
