from __future__ import print_function

import sqlite3

from Constants import *


class DatabaseAccessor(object):
    WHEEL_LAP_TIMES_TABLE_NAME = "wheel_lap_times"
    BALL_LAP_TIMES_TABLE_NAME = "ball_lap_times"

    __instance__ = None
    connect = None

    @staticmethod
    def get_instance():
        if DatabaseAccessor.__instance__ is None:
            DatabaseAccessor.__instance__ = DatabaseAccessor()
        return DatabaseAccessor.__instance__

    def __init__(self):
        self.connect = sqlite3.connect(Constants.DATABASE_NAME)

    @classmethod
    def insert_ball_lap_times(cls, session_id, lap_time):
        print("insert_ballLap_times, session_id = " + session_id + ", laptime = " + lap_time)
        cls.insert(cls.BALL_LAP_TIMES_TABLE_NAME, session_id, lap_time)

    @classmethod
    def insert_wheel_lap_times(cls, session_id, lap_time):
        print("insert_wheelLap_times, session_id = " + session_id + ", laptime = " + lap_time)
        cls.insert(cls.WHEEL_LAP_TIMES_TABLE_NAME, session_id, lap_time)

    @classmethod
    def insert(cls, table_name, session_id, lap_time):
        query = "INSERT INTO `" + table_name + "` (`ID`, `SESSION_ID`, `TIME`) VALUES (NULL, '" + \
                session_id + "', '" + lap_time + "');"
        cls.exec_query(query)

    @classmethod
    def increment_and_get_session_id(cls):
        query = "INSERT INTO `session` (`ID`) VALUES (NULL);"
        cls.exec_query(query)
        return cls.get_last_session_id()

    @classmethod
    def get_outcome(cls, session_id):
        query = "SELECT * FROM `outcomes` WHERE SESSION_ID = " + session_id + ";"
        for row in cls.connect.execute(query):
            return row['NUMBER']

    @classmethod
    def get_session_ids(cls):
        ids = []
        for row in cls.connect.execute("SELECT ID from session ORDER BY id DESC LIMIT 1"):
            ids.append(row['ID'])
        return ids

    @classmethod
    def get_last_session_id(cls):
        for row in cls.connect.execute("SELECT ID from session ORDER BY id DESC LIMIT 1"):
            return row['ID']

    @classmethod
    def select_ball_lap_times(cls, session_id):
        return cls.select_lap_times(cls.BALL_LAP_TIMES_TABLE_NAME, session_id)

    @classmethod
    def select_wheel_lap_times(cls, session_id):
        return cls.select_lap_times(cls.WHEEL_LAP_TIMES_TABLE_NAME, session_id)

    @classmethod
    def select_lap_times(cls, table_name, session_id):
        sql_query = "SELECT TIME FROM `" + table_name + "` WHERE SESSION_ID = " + session_id + ";"
        result = []
        for row in cls.connect.execute(sql_query):
            result.append(row['TIME'])
        return result

    @classmethod
    def close(cls):
        cls.connect.close()

    @classmethod
    def insert_outcome(cls, session_id, number):
        query = "INSERT INTO `outcomes` (`ID`, `SESSION_ID`, `NUMBER`) VALUES (NULL, '" + session_id \
                + "', '" + number + "');"
        cls.exec_query(query)

    @classmethod
    def exec_query(cls, sql_query):
        cls.connect.execute(sql_query)
        cls.connect.commit()
