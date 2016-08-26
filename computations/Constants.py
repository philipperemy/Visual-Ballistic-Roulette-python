#!/usr/bin/env python

from Wheel import Wheel

PI = 3.14159265359


class Constants(object):

    WHEEL_DIAMETER = 1
    CASE_DIAMETER = 1.0

    @staticmethod
    def get_wheel_circumference():
        return Constants.WHEEL_DIAMETER * PI

    @staticmethod
    def get_ball_circumference():
        return Constants.CASE_DIAMETER * PI

    class Type:
        def __init__(self):
            pass

        BALL = 'BALL'
        WHEEL = 'WHEEL'

    MIN_NUMBER_OF_WHEEL_TIMES_BEFORE_PREDICTION = 2
    MIN_NUMBER_OF_BALL_TIMES_BEFORE_PREDICTION = 3
    THRESHOLD_BEFORE_NEW_SESSION_IN_MS = 30 * 1000

    #  There is only one way we accept in the games. Never change this.
    DEFAULT_WHEEL_WAY = Wheel.WheelWay.ANTICLOCKWISE
    DATABASE_NAME = 'roulette-experiment.db'
    SECONDS_NEEDED_TO_PLACE_BETS = 0

    #  Physics
    DIFF_TIMES = 2.42 - 0.05
    DEFAULT_SHIFT_PHASE = 37
