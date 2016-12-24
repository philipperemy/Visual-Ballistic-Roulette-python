from Wheel import Wheel


class Constants(object):
    # Hyper parameters.
    EXPECTED_BOUNCING_SHIFT_FORWARD_DIAMOND = 16
    EXPECTED_BOUNCING_SHIFT_BLOCKER_DIAMOND = 6
    NEAREST_NEIGHBORS_COUNT = 3
    BIAS_MOVE_TO_NEXT_DIAMOND = 0  # due to the intrinsic speed. might change something. to be removed maybe later.

    class Type:
        def __init__(self):
            pass

        BALL = 'BALL'
        WHEEL = 'WHEEL'

    MIN_WHEEL_COUNT_OF_RECORDED_TIMES = 2
    MIN_BALL_COUNT_OF_RECORDED_TIMES = 3
    THRESHOLD_BEFORE_NEW_SESSION_IN_MS = 30 * 1000

    #  There is only one way we accept in the games. Never change this.
    DEFAULT_WHEEL_WAY = Wheel.WheelWay.CLOCKWISE
    DATABASE_NAME = 'roulette-experiment.db'
    SECONDS_NEEDED_TO_PLACE_BETS = 0
