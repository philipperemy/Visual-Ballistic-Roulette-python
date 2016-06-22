from __future__ import print_function

from Exceptions import *


class Wheel(object):
    #
    # 	 * Roulette numbers represented as a 1D-vector. Each number is accessed with
    # 	 * its index. Arithmetic operations are made on the indexes. For example.
    # 	 * Index of 0 is 0. Index of 32 is 1. Distance(0,32) = 1 - 0 = 1
    # 	 
    NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9,
               22, 18, 29, 7, 28, 12, 35, 3, 26]

    class WheelWay:
        def __init__(self):
            pass

        CLOCKWISE = 'CLOCKWISE'
        ANTICLOCKWISE = 'ANTICLOCKWISE'

    # * Calculate a valid index from Z -> [0, 36] (length = 37 numbers)
    # 	 * 
    # 	 * @param any integer
    # 	 * @return valid index
    @staticmethod
    def get_index(index):
        count_wheel_numbers = len(Wheel.NUMBERS)
        while index < 0:
            index += count_wheel_numbers
        while index >= count_wheel_numbers:
            index -= count_wheel_numbers
        return index

    # 
    # 	 * Calculate the region around a specific number. Example is:
    # 	 * region(reference_number=32, half_size = 2) = [26,0,32,15,19]
    # 	 
    @staticmethod
    def get_nearby_numbers(reference_number, half_size):
        idx_number = Wheel.find_index_of_number(reference_number)
        first_idx_number = Wheel.get_index(idx_number - half_size)
        num_of_elements = half_size * 2 + 1
        nearby_numbers = Wheel.NUMBERS[first_idx_number:first_idx_number + num_of_elements]
        return nearby_numbers

    # 
    # 	 * Translates a number on the wheel by a specific value.
    # 	 * 
    # 	 * @param reference_number
    # 	 *            The number on the wheel
    # 	 * @param phase_count
    # 	 *            How many pockets should the reference number be translated
    # 	 * @param way
    # 	 *            Clockwise or Anticlockwise
    # 	 * @return Example is translated(reference_number=32, phase_count=2,
    # 	 *         way=Anticlockwise) = 19 ATTENTION: This is a bit tricky because
    # 	 *         when the wheel turns anticlockwise, we scan the numbers forward
    # 	 *         and not backwards as we would imagine. Sketch something if you
    # 	 *         ain't sure.
    # 	 
    @staticmethod
    def get_number_with_phase(reference_number, phase_count, way):
        idx_reference_number = Wheel.find_index_of_number(reference_number)
        if way == Wheel.WheelWay.CLOCKWISE:
            new_idx = idx_reference_number - phase_count
        elif way == Wheel.WheelWay.ANTICLOCKWISE:
            new_idx = idx_reference_number + phase_count
        else:
            raise CriticalException("Unknown type.")
        return Wheel.NUMBERS[Wheel.get_index(new_idx)]

    # 
    # 	 * Example is: Give me the index of the number 32. Answer is 1.
    # 	 
    @staticmethod
    def find_index_of_number(number):
        return Wheel.NUMBERS.index(number)

    # 
    # 	 * Calculates the translation between (phase1, outcome1) and applies this
    # 	 * translation to phase2. Example is: phase1 = 0, outcome1 = 32. phase2 =
    # 	 * 19. translation(phase1, outcome1) = you add 1 forward. You take the
    # 	 * number 19 and you add this translation. The result is 4.
    # 	 
    @staticmethod
    def predict_outcome_with_shift(phase1, outcome1, phase2):
        """ generated source for method predict_outcomeWith_shift """
        idx_p1 = Wheel.find_index_of_number(phase1)
        idx_o1 = Wheel.find_index_of_number(outcome1)
        diff_idx_between_phase_and_outcome1 = Wheel.get_index(idx_o1 - idx_p1)
        id_p2 = Wheel.find_index_of_number(phase2)
        id_o2 = Wheel.get_index(id_p2 + diff_idx_between_phase_and_outcome1)
        return Wheel.NUMBERS[id_o2]

    # 
    # 	 * Here max distance is 37/2. Opposite of the wheel. Calculate the shortest
    # 	 * distance between two numbers. Example: distance(0,32) = 1.
    # 	 
    @staticmethod
    def distance_between_numbers(number1, number2):
        """ generated source for method distance_betweenNumbers """
        idx1 = Wheel.find_index_of_number(number1)
        idx2 = Wheel.find_index_of_number(number2)
        diff = abs(idx1 - idx2)
        diff_to_max_len = len(Wheel.NUMBERS) - diff
        return diff if diff < diff_to_max_len else diff_to_max_len
