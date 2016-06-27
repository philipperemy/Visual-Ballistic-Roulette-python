#!/usr/bin/env python

import sys
import time

from scipy.optimize import minimize


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *
from computations.predictor.physics.constantdeceleration.PredictorPhysicsConstantDeceleration import *


def current_time_millis():
    return int(round(time.time() * 1000))


BLT_PER_SESSION_ID = dict()
WLT_PER_SESSION_ID = dict()

da = DatabaseAccessor()
for session_id in da.get_session_ids():
    BLT_PER_SESSION_ID[session_id] = da.select_ball_lap_times(session_id)
    WLT_PER_SESSION_ID[session_id] = da.select_wheel_lap_times(session_id)


def function_to_minimize(x):
    import computations.Constants
    Constants.CUTOFF_SPEED = x[0]
    Constants.DEFAULT_SHIFT_PHASE = x[1]
    Constants.WHEEL_DIAMETER = x[2]
    Constants.CASE_DIAMETER = x[2] * 1.255  # ratio.
    reload(computations.Constants)
    dists_all = []
    for remove_ball_lap_id_from_end in range(0, 6, 1):
        dists = []
        for session_id in da.get_session_ids():
            if remove_ball_lap_id_from_end == 0:
                blt = BLT_PER_SESSION_ID[session_id]
            else:
                blt = BLT_PER_SESSION_ID[session_id][:-remove_ball_lap_id_from_end]
            wlt = WLT_PER_SESSION_ID[session_id]
            try:
                n_predicted = PredictorPhysicsConstantDeceleration.predict_most_probable_number(blt, wlt, debug=False)
                n_expected = da.get_outcome(session_id)
                dist = Wheel.distance_between_numbers(n_predicted, n_expected)
                dists.append(dist)
                dists_all.append(dist)
            except Exception as e:
                pass
                # print('remove_ball_lap_id_from_end = {}'.format(remove_ball_lap_id_from_end))
                # print('{} with len = {}'.format(dists, len(dists)))
                # print(np.mean(np.array(dists)))

    loss = np.mean(np.array(dists_all))
    print('cs = {}, dsp = {}, wd = {}, cd = {}, loss = {}'.format(Constants.CUTOFF_SPEED,
                                                                  Constants.DEFAULT_SHIFT_PHASE,
                                                                  Constants.WHEEL_DIAMETER,
                                                                  Constants.CASE_DIAMETER,
                                                                  loss))
    return loss


if __name__ == '__main__':
    x0 = (Constants.CUTOFF_SPEED, Constants.DEFAULT_SHIFT_PHASE, Constants.WHEEL_DIAMETER)
    res = minimize(fun=function_to_minimize, x0=x0, method='Nelder-Mead')
