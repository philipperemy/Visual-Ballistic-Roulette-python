#!/usr/bin/env python
""" generated source for module Session_manager """
from __future__ import print_function

from Constants import *


#  * A session corresponds to a game played or measured
class SessionManager(object):
    instance_ = None
    database = None
    timestamp_ofLast_query = 0

    def init(self, da):
        self.database = da

    @classmethod
    def get_instance(cls):
        if cls.instance_ is None:
            cls.instance_ = SessionManager()
        return cls.instance_

    def __init__(self):
        pass

    # * Every time a new lap time (ball or wheel) is submitted, we check if 30
    # 	 * seconds have elapsed. If this is the case, it means that this is a new
    # 	 * game and we should increment the session ID. If not, we just add it
    # 	 * normally.
    def call_manager(self, query_time):
        if query_time - self.timestamp_ofLast_query > Constants.THRESHOLD_BEFORE_NEW_SESSION_IN_MS:
            #  Start new session
            new_session_id = self.database.increment_and_get_session_id()
            print("Starting new session with id = " + new_session_id)
        else:
            new_session_id = self.database.get_last_session_id()
        # update time of last query
        self.timestamp_ofLast_query = query_time
        return new_session_id
