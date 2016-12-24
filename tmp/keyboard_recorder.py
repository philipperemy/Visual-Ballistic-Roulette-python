from __future__ import print_function

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


Constants.DATABASE_NAME = 'keyboard-recorder.db'
da = DatabaseAccessor()

if __name__ == '__main__':
    session_id = da.increment_and_get_session_id()
    print(session_id)
    while True:
        raw_input('')
        millis = current_time_millis()
        print(millis),
        da.insert_ball_lap_times(session_id, millis)

da.close()