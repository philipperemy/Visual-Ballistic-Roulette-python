#!/usr/bin/env python

import sys
import time


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


# -13.5%
# cs = 0.89377152252, dsp = 7.48843073348, wd = 0.547, cd = 0.687, loss = 8.13082437276, len = 558
# cs = 1.0535816322, dsp = 11.6969344401, wd = 0.547, cd = 0.687, loss = 8.09322033898, len = 472
def mcmc(fun, x0, max_iter=100):
    chains = np.zeros((max_iter, len(x0)))
    sigmas = np.array([0.2, 1])
    chains[0, :] = np.array(x0)
    l_prev = function_to_minimize(x0)
    for i in range(1, max_iter):
        new_prop = chains[i - 1, :] + sigmas * np.random.normal(0, 1, len(x0))
        l = function_to_minimize(list(new_prop))
        # if np.random.random(1) < np.exp(l_prev - l):
        if l < l_prev:
            chains[i, :] = new_prop
            l_prev = l
            print('chain = {}, loss = {}'.format(chains[i, :], l_prev))
        else:
            chains[i, :] = chains[i - 1, :]


def function_to_minimize(x):
    import computations.Constants
    Constants.CUTOFF_SPEED = x[0]
    Constants.DEFAULT_SHIFT_PHASE = x[1]
    # Constants.WHEEL_DIAMETER = x[2]
    # Constants.CASE_DIAMETER = x[2] * 1.255  # ratio.
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
    print('cs = {}, dsp = {}, wd = {}, cd = {}, loss = {}, len = {}'.format(Constants.CUTOFF_SPEED,
                                                                            Constants.DEFAULT_SHIFT_PHASE,
                                                                            Constants.WHEEL_DIAMETER,
                                                                            Constants.CASE_DIAMETER,
                                                                            loss,
                                                                            len(dists_all)))
    return loss


if __name__ == '__main__':
    PredictorPhysicsConstantDeceleration.load_cache(database=da)

    while True:
        s = np.random.uniform(1, 2)
        p = np.random.uniform(0, 35)
        x0 = (s, p)
        mcmc(fun=function_to_minimize, x0=(1.0, 11))
        # res = minimize(fun=function_to_minimize, x0=x0, method='Nelder-Mead')
