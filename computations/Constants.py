from Wheel import Wheel


class Constants(object):
    # constants to optimise.
    EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND = 16
    EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND = 6
    NEAREST_NEIGHBORS_COUNT = 3
    MOVE_TO_NEXT_DIAMOND = 0  # due to the intrinsic speed. might change something. to be removed maybe later.

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
