from computations.PredictorPhysics import *
from database.DatabaseAccessor import *

da = DatabaseAccessor.get_instance()

session_id = da.increment_and_get_session_id()

blocker_diamond_hit_time = 21.716
BS = np.array(
    [4.76, 5.28, 5.76, 6.24, 6.76, 7.28, 7.84, 8.44, 9.04, 9.68, 10.36, 11.08, 11.84, 12.72, 13.72, 15.04, 16.56,
     18.32, 20.36, blocker_diamond_hit_time]) * 1000
WS = np.array([1.08, 6.4, 11.6, 17, 22.44, 28]) * 1000
for bs in BS:
    da.insert_ball_lap_times(session_id, bs)
for ws in WS:
    da.insert_wheel_lap_times(session_id, ws)

PredictorPhysics.load_cache(da)
PredictorPhysics.predict_most_probable_number(BS[:-4], WS, debug=True)
