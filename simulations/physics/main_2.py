from computations.PredictorPhysics import *
from computations.comp_utils.Measures import AngularMeasure
from database.DatabaseAccessor import *
# from simulations.data_generation_8_b_w_fake_do_not_use_easier_problem import next_batch
from simulations.data_generation_10_b_w import next_batch


def test():
    DEBUG = True
    try:
        os.remove('roulette-experiment.db')
    except FileNotFoundError:
        pass
    da = DatabaseAccessor.get_instance()
    np.random.seed(126)
    nb = next_batch(debug=DEBUG)
    session_id = da.increment_and_get_session_id()
    bs_list = np.append(nb['abs_ball_times'], nb['abs_cutoff_time']) * 1000
    ws_list = np.array(nb['abs_wheel_times']) * 1000

    print(bs_list)
    print(ws_list)

    for bs in bs_list:
        da.insert_ball_lap_times(session_id, bs)
    for ws in ws_list:
        da.insert_wheel_lap_times(session_id, ws)

    PredictorPhysics.load_cache(da)
    num_cutoff, _ = PredictorPhysics.predict_most_probable_number(bs_list[:-3], ws_list, debug=DEBUG)
    e = AngularMeasure(nb['number_cutoff'], num_cutoff).error()
    print(e)


if __name__ == '__main__':
    test()
