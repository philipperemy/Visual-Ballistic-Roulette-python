import sys
import time

from PredictorPhysics import *


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *


def current_time_millis():
    return int(round(time.time() * 1000))

BS = [1000]
for i in range(10):
    BS.append(BS[-1] * 1.1)
WS = np.array([0, 3, 6, 9]) * 1000

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

PredictorPhysics.load_cache(da)

BS_i = BS[2:-5]
PredictorPhysics.predict_most_probable_number(BS_i, WS, debug=True)
