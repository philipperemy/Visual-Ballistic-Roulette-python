import sys
import time


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *


def current_time_millis():
    return int(round(time.time() * 1000))


da = DatabaseAccessor()

for session_id in range(5):
    for bs in range(20):
        da.insert_ball_lap_times(session_id, current_time_millis())
    for ws in range(5):
        da.insert_wheel_lap_times(session_id, current_time_millis())
