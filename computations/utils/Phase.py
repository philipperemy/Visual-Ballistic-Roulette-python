import numpy as np

from computations.Wheel import Wheel


class Phase(object):
    #
    # 	We want to find the number of the wheel where the ball passes in front of the mark.
    #
    # 	@param time_of_ball_in_front_of_mark last time in seconds when the balls passes in front of the mark.
    # 	@param time_of_wheel_in_front_of_mark last time in seconds when the zero of the wheel is in front of the mark.
    # 	@param wheel_revolution_time last known revolution time of the wheel.
    # 	@param way always ANTICLOCKWISE (despite the fact the clockwise way was implemented)
    # 	@return the number that is aligned with the mark when the ball was in front of the mark at time
    #  time_of_ball_in_front_of_landmark.
    #
    @staticmethod
    def find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                 time_of_wheel_in_front_of_mark,
                                                 wheel_revolution_time,
                                                 way):
        diff_time = np.abs(time_of_ball_in_front_of_mark - time_of_wheel_in_front_of_mark)
        numbers_count = len(Wheel.NUMBERS)
        idx_phase = int((diff_time / wheel_revolution_time * numbers_count))
        idx_zero = Wheel.find_index_of_number(0)  # Should be always 0
        if time_of_ball_in_front_of_mark > time_of_wheel_in_front_of_mark:
            #  t(Wheel) < t(Ball) Wheel is ahead of phase
            #  The question is: what is the value of the wheel when the ball
            #  is in front of the mark?
            if way == Wheel.WheelWay.CLOCKWISE:
                idx = idx_zero - idx_phase
            elif way == Wheel.WheelWay.ANTICLOCKWISE:
                idx = idx_zero + idx_phase
            else:
                raise Exception("Unknown type.")
        else:
            #  t(Wheel) > t(Ball) Ball is ahead of phase
            #  The question is what is the value of the ball when the wheel
            #  is in front of the wheel?
            if way == Wheel.WheelWay.CLOCKWISE:
                idx = idx_zero + idx_phase
            elif way == Wheel.WheelWay.ANTICLOCKWISE:
                idx = idx_zero - idx_phase
            else:
                raise Exception("Unknown type.")
        return Wheel.NUMBERS[Wheel.get_index(idx)]
