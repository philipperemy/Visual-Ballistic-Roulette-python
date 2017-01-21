import sys
import time

from computations.PredictorPhysics import *


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/comp_utils")
    sys.path.append("./comp_utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *


def current_time_millis():
    return int(round(time.time() * 1000))


BS = np.array([02.183, 02.849, 03.566, 04.349, 05.166, 06.150, 07.383, 08.933, 10.733, 12.683, 14.916]) * 1000
WS = np.array([05.066, 11.099, 17.299]) * 1000
# Final number is 6. Number at cutoff is 2.

BS_2 = np.array([09.583, 10.366, 11.249, 12.266, 13.566, 15.216, 17.033, 19.116, 21.450]) * 1000
WS_2 = np.array([11.049, 17.233]) * 1000
# Final number is 15. Number at cutoff is 20. Hit FORWARD + BLOCKER.

BS_3 = np.array([03.516, 04.299, 05.166, 06.166, 07.483, 09.150, 10.999, 13.083]) * 1000
WS_3 = np.array([05.499, 12.299]) * 1000
# Final number is 21. Number at cutoff is 23. Hit FORWARD.
# Time left is 15.333 - 13.083 = 2.25 (one loop left exactly!)

BS_4 = np.array([00.550, 01.083, 01.466, 01.983, 02.499, 03.083, 03.599, 04.199, 04.799, 05.499, 06.199, 06.950, 07.750,
                 08.633, 09.583, 10.850, 12.483, 14.266, 16.316]) * 1000
WS_4 = np.array([02.566, 07.933, 13.366]) * 1000
# Final number is 18. phase at cutoff is 22.
# Time left is 18.183 - 16.316 = 1.86 seconds.
# Number of revolutions left is 7/8 = 0.875.

try:
    os.remove(Constants.DATABASE_NAME)
except OSError:
    pass

da = DatabaseAccessor()

session_id = da.increment_and_get_session_id()

for bs in BS:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS:
    da.insert_wheel_lap_times(session_id, ws)

session_id = da.increment_and_get_session_id()

for bs in BS_2:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS_2:
    da.insert_wheel_lap_times(session_id, ws)

session_id = da.increment_and_get_session_id()

for bs in BS_3:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS_3:
    da.insert_wheel_lap_times(session_id, ws)

session_id = da.increment_and_get_session_id()

for bs in BS_4:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS_4:
    da.insert_wheel_lap_times(session_id, ws)

# we can do even easier. recreate the whole curve and find the xmin such that f(xmin) = times_cutoff.
# then identify how long left with TS Merge.

PredictorPhysics.load_cache(da)
# PredictorPhysics.predict_most_probable_number(BS_2[:-1], WS_2, debug=True)

PredictorPhysics.predict_most_probable_number(BS_4[:-1], WS_4, debug=True)
