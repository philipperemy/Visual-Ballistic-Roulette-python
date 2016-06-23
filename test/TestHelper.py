import unittest

from computations.predictor.Phase import *
from computations.utils.Helper import *


class TestHelper(unittest.TestCase):
    def test_convert_to_seconds(self):
        self.assertListEqual([1.0, 1.01, 1.02], Helper.convert_to_seconds([1000.0, 1010.0, 1020.0]))

    def test_print(self):
        self.assertEqual('+oo', Helper.print_val_or_infinity_symbol(30000000000))
        self.assertEqual('305', Helper.print_val_or_infinity_symbol(305))

    def test_last_value_in_front_ref(self):
        wheel_lap_times = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
        ball_lap_time_in_front_of_ref = 12.5
        self.assertEqual(12.0,
                         Helper.get_last_time_wheel_is_in_front_of_ref(wheel_lap_times, ball_lap_time_in_front_of_ref))

    def test_compute_diff(self):
        #  In meter/second
        cumsum_times = [10.0, 11.0, 12.0, 13.0, 15.0]
        self.assertListEqual([1.0, 1.0, 1.0, 2.0], list(Helper.compute_diff(cumsum_times)))

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
        time_of_ball_in_front_of_mark = 61564 * 0.001
        time_of_wheel_in_front_of_mark = 60882 * 0.001
        last_wheel_speed = Helper.get_wheel_speed(57196 * 0.001, 60882 * 0.001)
        phase_number = Phase.find_phase_number_between_ball_and_wheel(time_of_ball_in_front_of_mark,
                                                                      time_of_wheel_in_front_of_mark, last_wheel_speed,
                                                                      Wheel.WheelWay.ANTICLOCKWISE)
        self.assertEqual(2, phase_number)

    #  Can predict the ball before the wheel passes by.
    def test_helper_strategy_5(self):
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
        self.assertEqual(1, Wheel.distance_between_numbers(17, 34))
        self.assertEqual(1, Wheel.distance_between_numbers(26, 0))
        self.assertEqual(1, Wheel.distance_between_numbers(0, 26))
        self.assertEqual(Wheel.distance_between_numbers(18, 34), Wheel.distance_between_numbers(34, 18))

    def test_distance_two_random_numbers(self):
        N = 1000000
        r = np.random.randint(len(Wheel.NUMBERS), size=(N, 2))
        dist = 0.0
        for i in range(N):
            dist += Wheel.distance_between_numbers(r[i, 0], r[i, 1])
        dist /= N
        print(dist)
        self.assertTrue(9.2 < dist < 9.3)
