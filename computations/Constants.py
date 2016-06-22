#!/usr/bin/env python
""" generated source for module Constants """
from __future__ import print_function

from Wheel import Wheel

PI = 3.14159265359


class Constants(object):
    # TODO: To be measured. All is in meters and seconds.
    WHEEL_DIAMETER = 0.547
    CASE_DIAMETER = 0.687

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
    DATABASE_NAME = 'roulette-test.db'
    TIME_LEFT_FOR_PLACING_BETS_SECONDS = 2

    #  Physics
    CUTOFF_SPEED = 0.75
    DEFAULT_SHIFT_PHASE = 77
