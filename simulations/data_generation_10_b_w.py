import warnings

import numpy as np
import pylab
from scipy.integrate import quad

from computations.Wheel import Wheel
from computations.comp_utils.Helper import Helper
from computations.comp_utils.Phase import Phase

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

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
    x = np.linspace(0, 15, 1000)
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


def generate_abs_times(circumference, cutoff_speed, init_max_time_value_first_ball_time):
    warnings.filterwarnings('error')
    cur_time = np.random.uniform(low=0.0, high=init_max_time_value_first_ball_time)
    abs_times = [cur_time]
    abs_cutoff_time = neg_exp_inv(cutoff_speed)
    while True:
        try:
            cur_time = find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, circumference, cur_time)
        except Exception:
            cur_time = np.nan
        if np.isnan(cur_time) or cur_time >= abs_cutoff_time:
            print('ground truth next abs time = {}'.format(cur_time))
            break
        abs_times.append(cur_time)
    warnings.filterwarnings('ignore')
    return np.array(abs_times), abs_cutoff_time


def get_real_number(ball_recorded_time, last_wheel_recorded_time, wheel_last_revolution_time):
    return Phase.find_phase_number_between_ball_and_wheel(ball_recorded_time,
                                                          last_wheel_recorded_time,
                                                          wheel_last_revolution_time,
                                                          Wheel.WheelWay.CLOCKWISE)


def get_number(t, initial_number, rev_time):
    res_t = (t % rev_time) / rev_time
    shift_to_add = res_t * len(Wheel.NUMBERS)
    return Wheel.get_number_with_shift(initial_number, shift_to_add, Wheel.WheelWay.CLOCKWISE)


def test_wheel():
    initial_number = np.random.choice(Wheel.NUMBERS)
    rev_time = 3
    np.testing.assert_almost_equal(get_number(rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(2 * rev_time, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(0, initial_number, rev_time), initial_number)
    np.testing.assert_almost_equal(get_number(rev_time / 2, 0, rev_time), [5])
    np.testing.assert_almost_equal(get_number(rev_time / 2, 10, rev_time), [0])
    np.testing.assert_almost_equal(get_number(.001, 0, rev_time), [0])
    # at time 0, this is the initial number.
    # at time 3, should be again 0.


def test_ball():
    circ = 0.85 * np.pi
    abs_times, _ = generate_abs_times(circ, cutoff_speed=0.5, init_max_time_value_first_ball_time=1.0)
    # print(np.diff(abs_times))
    np.testing.assert_approx_equal(distance_travelled(abs_times[0], abs_times[1], neg_exp), circ)
    plot_f(neg_exp)

    np.testing.assert_approx_equal(5.0, neg_exp_inv(neg_exp(5.0)))
    np.testing.assert_almost_equal(distance_travelled(0.5, 1, neg_exp), distance_travelled_2(0.5, 1, neg_exp_F))
    # print(find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, 4.7581290982, 0))
    # ans = quad(neg_exp, 0, 1)
    # print(ans)


def generate_wheel_abs_times(rev_time, initial_number, max_len):
    # initial number already reflects the position of the wheel at the t=0 for the ball.
    cur_time = 0
    abs_times = []
    shift = -1
    for ii in range(len(Wheel.NUMBERS)):
        number = Wheel.get_number_with_shift(initial_number, ii, Wheel.WheelWay.CLOCKWISE)
        if number == 0:
            shift = ii
            break
    assert shift != -1
    cur_time += (shift / len(Wheel.NUMBERS)) * rev_time
    abs_times.append(cur_time)
    for jj in range(max_len):
        cur_time += rev_time
        abs_times.append(cur_time)
    return np.array(abs_times)


def next_batch(debug=True):
    circ = 0.85 * np.pi
    cutoff_speed = 1.0
    rev_time = 3  # units of time.
    init_max_time_value_first_ball_time = 1.0

    # BALL PART
    abs_ball_times, abs_cutoff_time = generate_abs_times(circ, cutoff_speed, init_max_time_value_first_ball_time)
    Wheel.find_index_of_number(0)
    abs_ball_times -= abs_ball_times[0]

    # WHEEL PART
    initial_number = np.random.choice(Wheel.NUMBERS)  # at time = 0
    abs_wheel_times = generate_wheel_abs_times(rev_time, initial_number, max_len=len(abs_ball_times))
    numbers = []
    for abs_ball_time in np.append(abs_ball_times, abs_cutoff_time):
        abs_wheel_time = Helper.get_last_time_wheel_is_in_front_of_ref(abs_wheel_times, abs_ball_time)
        if abs_wheel_time is None:
            numbers.append(None)
        else:
            num = get_real_number(abs_ball_time, abs_wheel_time, rev_time)
            assert num == get_number(abs_ball_time - abs_wheel_time, 0, rev_time)
            numbers.append(num)
    number_landmark_number_cutoff = numbers[-1]
    ball_distance_travelled = distance_travelled(abs_ball_times[-1], abs_cutoff_time, neg_exp)
    distance_percentage = (ball_distance_travelled % circ) / circ
    ball_cutoff_shift = distance_percentage * len(Wheel.NUMBERS)
    number_cutoff = Wheel.get_number_with_shift(number_landmark_number_cutoff, ball_cutoff_shift,
                                                Wheel.WheelWay.CLOCKWISE)

    numbers = np.array(numbers)[:-1]
    if debug:
        print('-' * 80)
        print('ABSOLUTE BALL TIMES       =', abs_ball_times)
        print('ABSOLUTE WHEEL TIMES      =', abs_wheel_times)
        print('ABS CUTOFF TIME           =', abs_cutoff_time)
        print('NUMBERS                   =', numbers)
        print('BALL CUTOFF SHIFT         =', ball_cutoff_shift)
        print('NUMBER CUTOFF             =', number_cutoff)
        print('DISTANCE PERC             =', distance_percentage)
        print('NUMBER LANDMARK AT CUTOFF =', number_landmark_number_cutoff)

    return {'abs_ball_times': abs_ball_times,
            'abs_wheel_times': abs_wheel_times,
            'abs_cutoff_time': abs_cutoff_time,
            'numbers': numbers,
            'number_landmark_number_cutoff': number_landmark_number_cutoff,
            'ball_cutoff_shift': ball_cutoff_shift,
            'distance_percentage': distance_percentage,
            'number_cutoff': number_cutoff}


if __name__ == '__main__':
    for jj in range(10):
        next_batch()
    test_wheel()
    test_ball()
