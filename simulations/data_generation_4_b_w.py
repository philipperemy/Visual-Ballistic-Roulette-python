import warnings
from time import sleep

import numpy as np
import pylab
from scipy.integrate import quad

from computations.Wheel import Wheel

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
warnings.filterwarnings('error')

a = 5.0
b = 8.0


def neg_exp_F(x):
    return - (a * b) * np.exp(-x / a)


def neg_exp_F_inv(x):
    return - a * np.log(-x / (a * b))


def neg_exp_inv(x):
    return -a * np.log(x / b)


def neg_exp(x):
    return np.exp(-x / a) * b


def plot_f(f):
    x = np.linspace(0, 30, 1000)
    y = f(x)
    pylab.plot(x, y)
    pylab.show()


def plot_a(a):
    pylab.plot(a)
    pylab.show()


def distance_travelled(t1, t2, f):
    (int_val, err) = quad(f, t1, t2)
    return int_val


def distance_travelled_2(t1, t2, F):
    return F(t2) - F(t1)


def find_upper_bound_for_given_integral_value(inv_F, F, int_value, start_value):
    return inv_F(int_value + F(start_value))


def generate_lap_times(circumference, cutoff_speed, init_max_time_value_first_ball_time):
    cur_time = np.random.uniform(low=0.0, high=init_max_time_value_first_ball_time)
    abs_times = [cur_time]
    abs_cutoff_time = neg_exp_inv(cutoff_speed)
    while True:
        try:
            cur_time = find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, circumference, cur_time)
        except Exception:
            cur_time = np.nan
        # print(cur_time)
        if np.isnan(cur_time) or cur_time >= abs_cutoff_time:
            break
        abs_times.append(cur_time)
    return np.array(abs_times), abs_cutoff_time


def get_number(t, initial_number, rev_time):
    res_t = t % rev_time
    shift_to_add = res_t * len(Wheel.NUMBERS)
    return Wheel.get_number_with_shift(initial_number, shift_to_add, Wheel.WheelWay.CLOCKWISE)


def test_wheel():
    initial_number = np.random.choice(Wheel.NUMBERS)
    rev_time = 3
    np.testing.assert_almost_equal(get_number(rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(2 * rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(0, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(rev_time / 2, 0, rev_time), [10])
    np.testing.assert_almost_equal(get_number(rev_time / 2, 10, rev_time), [26])
    np.testing.assert_almost_equal(get_number(.001, 0, rev_time), [0])
    # at time 0, this is the initial number.
    # at time 3, should be again 0.


def test_ball():
    circ = 0.85 * np.pi
    abs_times, _ = generate_lap_times(circ, cutoff_speed=0.5, init_max_time_value_first_ball_time=1.0)
    # print(np.diff(abs_times))
    np.testing.assert_approx_equal(distance_travelled(abs_times[0], abs_times[1], neg_exp), circ)
    plot_f(neg_exp)

    np.testing.assert_approx_equal(5.0, neg_exp_inv(neg_exp(5.0)))
    np.testing.assert_almost_equal(distance_travelled(0.5, 1, neg_exp), distance_travelled_2(0.5, 1, neg_exp_F))
    # print(find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, 4.7581290982, 0))
    # ans = quad(neg_exp, 0, 1)
    # print(ans)


def main():
    circ = 0.85 * np.pi
    cutoff_speed = 0.6
    rev_time = 3  # units of time.
    init_max_time_value_first_ball_time = 1.0  # 1 second max after t = 0.

    abs_times, abs_cutoff_time = generate_lap_times(circ, cutoff_speed, init_max_time_value_first_ball_time)
    abs_times -= abs_times[0]
    initial_number = np.random.choice(Wheel.NUMBERS)  # at time = 0
    numbers = []
    for abs_time in abs_times:
        numbers.append(get_number(abs_time, initial_number, rev_time))

    diff_times = np.diff(abs_times)
    print('-' * 80)
    print('ABSOLUTE TIMES   =', abs_times)
    print('LAP TIMES        =', diff_times)
    print('CUTOFF DIFF TIME =', abs_cutoff_time - abs_times[-1])
    print('NUMBERS          =', np.array(numbers))
    print('NUMBER CUTOFF    =', get_number(abs_cutoff_time, initial_number, rev_time))
    # plot_a(diff_times)
    sleep(0.1)


if __name__ == '__main__':
    for jj in range(10):
        main()
    test_wheel()
    test_ball()
