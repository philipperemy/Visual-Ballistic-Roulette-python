#!/usr/bin/env python

from Wheel import Wheel

PI = 3.14159265359


class Constants(object):
    # to change.
    WHEEL_DIAMETER = 0.5
    CASE_DIAMETER = 0.7

    @staticmethod
    def get_wheel_circumference():
        return Constants.WHEEL_DIAMETER * PI

    @staticmethod
    def get_ball_track_circumference():
        return Constants.CASE_DIAMETER * PI

    class DiamondType:
        def __init__(self):
            pass

        BLOCKER = 'BLOCKER'
        FORWARD = 'FORWARD'
        NONE = 'NONE'

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
    CUTOFF_SPEED = 1.00
    DEFAULT_SHIFT_PHASE = 37
