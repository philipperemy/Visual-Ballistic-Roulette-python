from computations.PredictorPhysics import *
from database.DatabaseAccessor import *
from read_results import read_experimentation_results, assert_equals
from computations.comp_utils.Measures import *

if __name__ == '__main__':
    try:
        os.remove('roulette-experiment.db')
    except:
        pass

    da = DatabaseAccessor.get_instance()

    predictions = read_experimentation_results()

    for predicted in predictions:
        new_session_id = da.increment_and_get_session_id()
        assert_equals(str(new_session_id), predicted['video_id'])
        for bs in predicted['ball_lap_times']:
            da.insert_ball_lap_times(new_session_id, float(bs) * 1000)
        for ws in predicted['wheel_lap_times']:
            da.insert_ball_lap_times(new_session_id, float(ws) * 1000)

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
    failures = 0.0
    predicted_numbers = []
    for predicted in predictions:
        BS = np.array(predicted['ball_lap_times']) * 1000
        WS = np.array(predicted['wheel_lap_times']) * 1000

        try:
            number = PredictorPhysics.predict_most_probable_number(BS[:-4], WS, debug=True)
            predicted_numbers.append(number)
        except:
            failures += 1.0

    expected_numbers = []
    for predicted in predictions:
        expected_number = da.get_outcome(predicted['video_id'])
        expected_numbers.append(expected_number)

    errors = []
    for (e, p) in zip(expected_numbers, predicted_numbers):
        errors.append(AngularMeasure(e, p).error())

    print('errors =', errors)
    print('errors mean =', np.mean(errors))
    print('total failures = {}'.format(float(failures) / len(predictions)))
