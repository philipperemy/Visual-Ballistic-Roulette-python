import numpy as np

from computations.Constants import *


class Diamonds(object):
    class DiamondType:
        BLOCKER = 'BLOCKER'
        FORWARD = 'FORWARD'
        NONE = 'NONE'

    @staticmethod
    def detect_diamonds(distance_left):
        """The beginning is assumed to be at the ref diamond. Ref diamond is FORWARD.
        8 diamonds in total. We consider 9 here just to have the modulo to 1 (close the loop).
        For example, if we have distance_left = 0.99, we consider it to be close to 1
        => First diamond should be hit. And not the last one equal to 7/8 = 0.875
        Ball is going anti-clockwise"""
        res_distance_left = distance_left % 1
        diamond_angles = np.cumsum(np.ones(9) * 1.0 / 8) - 1.0 / 8

        # 5 is a big value to be sure to be inside the bounds of diamond_types[]
        diamond_types = [Diamonds.DiamondType.FORWARD, Diamonds.DiamondType.BLOCKER] * 5
        distance_from_diamonds = np.square(np.array(diamond_angles - res_distance_left))
        index = np.argmin(distance_from_diamonds) + Constants.BIAS_MOVE_TO_NEXT_DIAMOND
        return diamond_types[index]
