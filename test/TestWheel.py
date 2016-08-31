import unittest

from Phase import *


class TestWheel(unittest.TestCase):
    def test_wheel(self):
        self.assertEqual(0, Wheel.find_index_of_number(0))
        self.assertEqual(len(Wheel.NUMBERS) - 1, Wheel.find_index_of_number(26))
        self.assertEqual(2, Wheel.find_index_of_number(15))
        self.assertListEqual([26, 0, 32], Wheel.get_nearby_numbers(0, 1))
        self.assertListEqual([2, 25, 17, 34, 6], Wheel.get_nearby_numbers(17, 2))
        self.assertEqual(26, Wheel.get_number_with_shift(0, 1, Wheel.WheelWay.CLOCKWISE))
        self.assertEqual(32, Wheel.get_number_with_shift(0, 1, Wheel.WheelWay.ANTICLOCKWISE))
        self.assertEqual(2, Wheel.get_number_with_shift(17, 2, Wheel.WheelWay.CLOCKWISE))
        self.assertEqual(6, Wheel.get_number_with_shift(17, 2, Wheel.WheelWay.ANTICLOCKWISE))

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
