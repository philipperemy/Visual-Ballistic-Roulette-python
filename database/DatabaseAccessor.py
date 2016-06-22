from __future__ import print_function

import sqlite3

from Constants import *


class DatabaseAccessor(object):
    WHEEL_LAP_TIMES_TABLE_NAME = "wheel_lap_times"
    BALL_LAP_TIMES_TABLE_NAME = "ball_lap_times"

    __instance__ = None

    @staticmethod
    def get_instance():
        if DatabaseAccessor.__instance__ is None:
            DatabaseAccessor.__instance__ = DatabaseAccessor()
        return DatabaseAccessor.__instance__

    def __init__(self):
        self.connect = sqlite3.connect(Constants.DATABASE_NAME, check_same_thread=False)
        self.exec_query('CREATE TABLE IF NOT EXISTS `session` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT)')
        self.exec_query('CREATE TABLE IF NOT EXISTS `ball_lap_times` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT, `SESSION_ID` int(10) NOT NULL, `TIME` varchar(255) NOT NULL)')
        self.exec_query('CREATE TABLE IF NOT EXISTS `clockwise` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT, `CLOCKWISE` int(11) NOT NULL, `SESSION_ID` int(11) NOT NULL)')
        self.exec_query('CREATE TABLE IF NOT EXISTS `outcomes` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT, `SESSION_ID` int(10) NOT NULL, `NUMBER` varchar(255) NOT NULL, `OBSTACLES` int(10) NOT NULL)')
        self.exec_query('CREATE TABLE IF NOT EXISTS `wheel_lap_times` (`ID` INTEGER PRIMARY KEY AUTOINCREMENT, `SESSION_ID` int(10) NOT NULL, `TIME` varchar(255) NOT NULL)')

    def insert_ball_lap_times(self, session_id, lap_time):
        print("insert_ball_lap_times, session_id = {}, lap time = {}".format(session_id, lap_time))
        self.insert(self.BALL_LAP_TIMES_TABLE_NAME, session_id, lap_time)

    def insert_wheel_lap_times(self, session_id, lap_time):
        print("insert_wheel_lap_times, session_id = {}, lap time = {}".format(session_id, lap_time))
        self.insert(self.WHEEL_LAP_TIMES_TABLE_NAME, session_id, lap_time)

    def insert(self, table_name, session_id, lap_time):
        query = "INSERT INTO `" + table_name + "` (`ID`, `SESSION_ID`, `TIME`) VALUES (NULL, '" + \
                str(session_id) + "', '" + str(lap_time) + "');"
        self.exec_query(query)

    def increment_and_get_session_id(self):
        query = "INSERT INTO `session` (`ID`) VALUES (NULL);"
        self.exec_query(query)
        return self.get_last_session_id()

    def get_outcome(self, session_id):
        query = "SELECT * FROM `outcomes` WHERE SESSION_ID = " + str(session_id) + ";"
        for row in self.connect.execute(query):
            return row['NUMBER']

    def get_session_ids(self):
        ids = []
        for row in self.connect.execute("SELECT ID from session ORDER BY id DESC LIMIT 1"):
            ids.append(row['ID'])
        return ids

    def get_last_session_id(self):
        for row in self.connect.execute("SELECT ID from session ORDER BY id DESC LIMIT 1"):
            return row[0]

    def select_ball_lap_times(self, session_id):
        return self.select_lap_times(self.BALL_LAP_TIMES_TABLE_NAME, session_id)

    def select_wheel_lap_times(self, session_id):
        return self.select_lap_times(self.WHEEL_LAP_TIMES_TABLE_NAME, session_id)

    def select_lap_times(self, table_name, session_id):
        sql_query = "SELECT TIME FROM `" + table_name + "` WHERE SESSION_ID = " + str(session_id) + ";"
        result = []
        for row in self.connect.execute(sql_query):
            result.append(row['TIME'])
        return result

    def close(self):
        self.connect.close()

    def insert_outcome(self, session_id, number):
        query = "INSERT INTO `outcomes` (`ID`, `SESSION_ID`, `NUMBER`, `OBSTACLES`) VALUES (NULL, '" + str(session_id) \
                + "', '" + str(number) + "', 0);"
        self.exec_query(query)

    def exec_query(self, sql_query):
        self.connect.execute(sql_query)
        self.connect.commit()


if __name__ == '__main__':
    tst = DatabaseAccessor()
    tst.increment_and_get_session_id()
    tst.insert_ball_lap_times(1, 123)
    tst.insert_wheel_lap_times(1, 124)
    tst.insert_outcome(1, 32)
