import numpy as np

from utils.Exceptions import *


class Wheel(object):
    # Roulette numbers represented as a 1D-vector. Each number is accessed with
    # its index. Arithmetic operations are made on the indexes. For example.
    # Index of 0 is 0. Index of 32 is 1. Distance(0,32) = 1 - 0 = 1
    # 	 
    NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9,
               22, 18, 29, 7, 28, 12, 35, 3, 26]

    class WheelWay:
        def __init__(self):
            pass

        CLOCKWISE = 'CLOCKWISE'
        ANTICLOCKWISE = 'ANTICLOCKWISE'

    # Calculate a valid index from Z -> [0, 36] (length = 37 numbers)
    # param any integer
    # return valid index
    @staticmethod
    def get_index(index):
        return index % len(Wheel.NUMBERS)

    @staticmethod
    def get_nearby_numbers(reference_number, half_size):
        """
        region(reference_number=32, half_size = 2) = [26,0,32,15,19]
        :param reference_number: number
        :param half_size: half size of the region
        :return: calculate the region around a specific number
        """
        idx_number = Wheel.find_index_of_number(reference_number)
        first_idx_number = Wheel.get_index(idx_number - half_size)
        num_of_elements = half_size * 2 + 1
        nearby_numbers = []
        for j in range(num_of_elements):
            nearby_numbers.append(Wheel.NUMBERS[Wheel.get_index(first_idx_number)])
            first_idx_number += 1
        return nearby_numbers

    @staticmethod
    def get_number_with_shift(reference_number, shift, way):
        """
        Translates a number on the wheel by a specific value.
        :param reference_number: The number on the wheel
        :param shift: How many pockets should the reference number be translated
        :param way: Clockwise or Anticlockwise
        :return: Shifted number. ATTENTION: This is a bit tricky because
        when the wheel turns anticlockwise, we scan the numbers forward
        and not backwards as we would imagine. Sketch something if you
        ain't sure.
        """
        shift = int(np.round(shift))
        idx_reference_number = Wheel.find_index_of_number(reference_number)
        if way == Wheel.WheelWay.CLOCKWISE:
            new_idx = idx_reference_number - shift
        elif way == Wheel.WheelWay.ANTICLOCKWISE:
            new_idx = idx_reference_number + shift
        else:
            raise CriticalException("Unknown type.")
        return Wheel.NUMBERS[Wheel.get_index(new_idx)]

    # Example is: Give me the index of the number 32. Answer is 1.
    @staticmethod
    def find_index_of_number(number):
        return Wheel.NUMBERS.index(number)

    # Here max distance is 37/2. Opposite of the wheel. Calculate the shortest
    # distance between two numbers. Example: distance(0,32) = 1.
    @staticmethod
    def distance_between_numbers(number1, number2):
        idx1 = Wheel.find_index_of_number(number1)
        idx2 = Wheel.find_index_of_number(number2)
        diff = abs(idx1 - idx2)
        return min(diff, len(Wheel.NUMBERS) - diff)