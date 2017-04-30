import numpy as np

from computations.Wheel import Wheel

numbers = Wheel.NUMBERS


def get_number(t2, initial_number, rev_time):
    res_t = t2 % rev_time
    shift_to_add = res_t * len(numbers)
    return Wheel.get_number_with_shift(initial_number, shift_to_add, Wheel.WheelWay.CLOCKWISE)


def test():
    print(numbers)
    initial_number = np.random.choice(numbers)
    rev_time = 3
    np.testing.assert_almost_equal(get_number(rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(2 * rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(0, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(rev_time / 2, 0, rev_time), [10])
    np.testing.assert_almost_equal(get_number(rev_time / 2, 10, rev_time), [26])
    np.testing.assert_almost_equal(get_number(.001, 0, rev_time), [0])
    # at time 0, this is the initial number.
    # at time 3, should be again 0.


if __name__ == '__main__':
    test()
