from computations.predictor.machinelearning.HelperMachineLearning import *
from utils.Logging import *


class PredictorMachineLearning(object):
    # factor that as it is common to Physics.

    CACHE = None

    @staticmethod
    def load_cache(database):

        for session_id in database.get_session_ids():
            ball_cumsum_times = Helper.convert_to_seconds(database.select_ball_lap_times())
            wheel_cumsum_times = Helper.convert_to_seconds(database.select_wheel_lap_times())

            if len(wheel_cumsum_times) == 0:
                log("Wheel cumsum times are empty for session id = {}. Ignoring this game.".format(session_id))
                continue

            if len(ball_cumsum_times) == 0:
                log("Ball cumsum times are empty for session id = {}. Ignoring this game.".format(session_id))
                continue

            for records in HelperMachineLearning.build_data_records(ball_cumsum_times, wheel_cumsum_times):
                for record in records:
                    outcome = database.get_outcome(session_id)
                    record['outcome'] = outcome
                    PredictorMachineLearning.CACHE = record

    @staticmethod
    def predict_most_probable_number(ball_cumsum_times, wheel_cumsum_times, database):

        if len(wheel_cumsum_times) < Constants.MIN_NUMBER_OF_WHEEL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        if len(ball_cumsum_times) < Constants.MIN_NUMBER_OF_BALL_TIMES_BEFORE_PREDICTION:
            raise SessionNotReadyException()

        # in seconds.
        ball_cumsum_times = Helper.convert_to_seconds(ball_cumsum_times)
        wheel_cumsum_times = Helper.convert_to_seconds(wheel_cumsum_times)

        if PredictorMachineLearning.CACHE is None:
            PredictorMachineLearning.load_cache(database)

        most_probable_number = PredictorMachineLearning.predict(ball_cumsum_times, wheel_cumsum_times,
                                                                database)
        return most_probable_number

    @staticmethod
    def predict(ball_cumsum_times, wheel_cumsum_times, database):
        return 0
