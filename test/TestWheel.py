import unittest

from Phase import *


class TestWheel(unittest.TestCase):
    def test_wheel(self):
        self.assertEqual(0, Wheel.find_index_of_number(0))
        self.assertEqual(len(Wheel.NUMBERS) - 1, Wheel.find_index_of_number(26))
        self.assertEqual(2, Wheel.find_index_of_number(15))
        self.assertListEqual([26, 0, 32], Wheel.get_nearby_numbers(0, 1))
        self.assertListEqual([2, 25, 17, 34, 6], Wheel.get_nearby_numbers(17, 2))
        self.assertEqual(26, Wheel.get_number_with_phase(0, 1, Wheel.WheelWay.CLOCKWISE))
        self.assertEqual(32, Wheel.get_number_with_phase(0, 1, Wheel.WheelWay.ANTICLOCKWISE))
        self.assertEqual(2, Wheel.get_number_with_phase(17, 2, Wheel.WheelWay.CLOCKWISE))
        self.assertEqual(6, Wheel.get_number_with_phase(17, 2, Wheel.WheelWay.ANTICLOCKWISE))

    def test_helper_speed(self):
        #  In meter/second
        self.assertEqual(Constants.get_ball_track_circumference(), Helper.get_ball_speed(0, 1), 0.01)
        self.assertEqual(Constants.get_wheel_circumference(), Helper.get_wheel_speed(0, 1), 0.01)

    def test_helper_strategy_2(self):
        """ generated source for method test_helperStrategy2 """
        #  Let assume we are at 5000.
        time_of_ball_in_front_of_mark = 5456 * 0.001
        time_of_wheel_in_front_of_mark = 6168 * 0.001
        last_wheel_speed = Helper.get_wheel_speed(2600 * 0.001, 6168 * 0.001)
        #  We want to find the number of the wheel where the ball passes in
        #  front of the mark.
        phase_number = Phase.find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                                      time_of_wheel_in_front_of_mark,
                                                                      last_wheel_speed,
                                                                      Wheel.WheelWay.ANTICLOCKWISE)
        self.assertEqual(29, phase_number)

    #  https://www.youtube.com/watch?v=nztu_ibJhq6o
    #  Second part of video. CLOCKWISE
    # 
    # 	 * REAL MEASURES
    # 	 * 
    # 	 * BALLS = 28184 28714 29323 29957 30832 31748 32825 34014 35326 36727 38277
    # 	 * 39924 41692 43643 45756
    # 	 * 
    # 	 * WHEELS = 27935 31866 35749 39723 43724 47751 51836
    # 	 * 
    def test_helper_strategy_3(self):
        #  Let assume we are at 35000.
        time_of_ball_in_front_of_mark = 35326 * 0.001
        time_of_wheel_in_front_of_mark = 35749 * 0.001
        last_wheel_speed = Helper.get_wheel_speed(31866 * 0.001, 35749 * 0.001)
        phase_number = Phase.find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                                      time_of_wheel_in_front_of_mark, last_wheel_speed,
                                                                      Wheel.WheelWay.CLOCKWISE)
        self.assertEqual(4, phase_number)

    def test_helper_strategy_4(self):
        #  Let assume we are at 57000.
        time_of_ball_in_front_of_mark = 61564 * 0.001
        time_of_wheel_in_front_of_mark = 60882 * 0.001
        last_wheel_speed = Helper.get_wheel_speed(57196 * 0.001, 60882 * 0.001)
        phase_number = Phase.find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                                      time_of_wheel_in_front_of_mark, last_wheel_speed,
                                                                      Wheel.WheelWay.ANTICLOCKWISE)
        self.assertEqual(2, phase_number)

    #  Can predict the ball before the wheel passes by.
    def test_helper_strategy_5(self):
        """ generated source for method test_helperStrategy5 """
        #  Let assume we are at 57000.
        time_of_ball_in_front_of_mark = 58547 * 0.001
        time_of_wheel_in_front_of_mark = 60882 * 0.001
        last_wheel_speed = Helper.get_wheel_speed(57196 * 0.001, 60882 * 0.001)
        phase_number = Phase.find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                                      time_of_wheel_in_front_of_mark, last_wheel_speed,
                                                                      Wheel.WheelWay.ANTICLOCKWISE)
        self.assertEqual(11, phase_number)
        #  11 is correct

    # 
    # 	 * 0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    # 	 * 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26 };
    # 	 
    def test_unit_tests(self):
        """ generated source for method unit_tests """
        self.assertEqual(1, Wheel.distance_between_numbers(17, 34))
        self.assertEqual(1, Wheel.distance_between_numbers(26, 0))
        self.assertEqual(1, Wheel.distance_between_numbers(0, 26))
        self.assertEqual(Wheel.distance_between_numbers(18, 34), Wheel.distance_between_numbers(34, 18))

    def test_distance_two_random_numbers(self):
        N = 100000
        r = np.random.randint(len(Wheel.NUMBERS), size=(N, 2))
        dist = 0.0
        for i in range(N):
            dist += Wheel.distance_between_numbers(r[i, 0], r[i, 1])
        dist /= N
        print(dist)
        self.assertTrue(9.2 < dist < 9.3)
