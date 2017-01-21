from computations.Constants import *
from utils.Logging import *


#  A session corresponds to a game played or measured
class SessionManager(object):
    database = None
    timestamp_of_last_query = 0

    def __init__(self, da):
        self.database = da

    # Every time a new lap time (ball or wheel) is submitted, we check if 30
    # seconds have elapsed. If this is the case, it means that this is a new
    # game and we should increment the session ID. If not, we just add it
    # normally.
    def call_manager(self, query_time):
        if query_time - self.timestamp_of_last_query > Constants.THRESHOLD_BEFORE_NEW_SESSION_IN_MS:
            #  Start new session
            new_session_id = self.database.increment_and_get_session_id()
            log("Starting new session with id = {}".format(new_session_id))
        else:
            new_session_id = self.database.get_last_session_id()
        # update time of last query
        self.timestamp_of_last_query = query_time
        return new_session_id
