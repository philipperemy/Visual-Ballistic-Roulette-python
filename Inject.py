import sys
import time

from computations.predictor.physics.constantdeceleration.PredictorPhysicsConstantDeceleration import *


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *
import numpy as np


def current_time_millis():
    return int(round(time.time() * 1000))


BS = np.array([08.433, 09.233, 10.166, 11.250, 12.583, 14.100, 15.816, 17.700, 19.850, 22.183]) * 1000
WS = np.array([12.166, 17.066, 21.983]) * 1000
# HIT 22.183. Phase is 15.

BS_2 = np.array([03.666, 04.250, 04.766, 05.366, 06.033, 06.683, 07.433, 08.216, 09.116, 10.166, 11.550, 13.283, 15.116,
                 17.283]) * 1000
WS_2 = np.array([03.316, 08.216, 13.450]) * 1000
# HIT 18.316. Phase is 36.

try:
    os.remove('roulette-experiment.db')
except OSError:
    pass

da = DatabaseAccessor()

session_id = da.increment_and_get_session_id()

for bs in BS:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS:
    da.insert_wheel_lap_times(session_id, ws)

session_id = da.increment_and_get_session_id()

da.increment_and_get_session_id()
for bs in BS_2:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS_2:
    da.insert_wheel_lap_times(session_id, ws)

# we can do even easier. recreate the whole curve and find the xmin such that f(xmin) = times_cutoff.
# then identify how long left with TS Merge.

PredictorPhysicsConstantDeceleration.load_cache(da)
PredictorPhysicsConstantDeceleration.predict_most_probable_number(BS[:-1], WS, debug=True)
PredictorPhysicsConstantDeceleration.predict_most_probable_number(BS[:-2], WS, debug=True)
PredictorPhysicsConstantDeceleration.predict_most_probable_number(BS[:-3], WS, debug=True)
PredictorPhysicsConstantDeceleration.predict_most_probable_number(BS[:-4], WS, debug=True)
PredictorPhysicsConstantDeceleration.predict_most_probable_number(BS[:-5], WS, debug=True)
# estimated time left is 22183-19850 = 2333.
