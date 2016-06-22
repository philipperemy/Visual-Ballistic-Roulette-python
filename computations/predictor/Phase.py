from __future__ import print_function

from Helper import *


class Phase(object):
    #
    # 	We want to find the number of the wheel where the ball passes in front of the mark.
    #
    # 	@param time_ofBall_inFront_ofMark last time in seconds when the balls passes in front of the mark.
    # 	@param time_ofWheel_inFront_ofMark last time in seconds when the zero of the wheel is in front of the mark.
    # 	@param last_wheelSpeed last known speed of the wheel.
    # 	@param way always ANTICLOCKWISE (despite the fact the clockwise way was implemented)
    # 	@return the number that is aligned with the mark when the ball was in front of the mark at time
    # time_ofBall_inFront_ofMark.
    # 	 
    @staticmethod
    def find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark, time_of_wheel_in_front_of_mark,
                                                 last_wheel_speed,
                                                 way):
        diff_time = np.abs(time_of_ball_in_front_of_mark - time_of_wheel_in_front_of_mark)
        wheel_revolution_time = Helper.get_time_for_one_wheel_loop(last_wheel_speed)
        numbers_count = Wheel.NUMBERS.length
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