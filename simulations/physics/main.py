from collections import deque

from computations.PredictorPhysics import *
from computations.comp_utils.Measures import AngularMeasure
from database.DatabaseAccessor import *
# from simulations.data_generation_8_b_w_fake_do_not_use_easier_problem import next_batch
from simulations.data_generation_9_b_w import next_batch

# error 2 with the real values. should be 0.
# the generator is not the best though.


def main():
    debug = True
    try:
        os.remove('roulette-experiment.db')
    except FileNotFoundError:
        pass
    da = DatabaseAccessor.get_instance()
    n = 2000
    average_error = deque(maxlen=50)
    for i in range(n):
        nb = next_batch(debug=debug)
        print('i =', i)
        session_id = da.increment_and_get_session_id()
        bs = np.append(nb['abs_ball_times'], nb['abs_cutoff_time']) * 1000
        ws = np.array(nb['abs_wheel_times']) * 1000

        if i == n // 2:
            PredictorPhysics.load_cache(da)

        if i < n // 2:
            for bs in bs:
                da.insert_ball_lap_times(session_id, bs)
            for ws in ws:
                da.insert_wheel_lap_times(session_id, ws)
        else:
            num_cutoff, _ = PredictorPhysics.predict_most_probable_number(bs[:-2], ws, debug=debug)
            e = AngularMeasure(nb['number_cutoff'], num_cutoff).error()
            average_error.append(e)
            print('average_error = ', np.mean(average_error))


if __name__ == '__main__':
    main()
