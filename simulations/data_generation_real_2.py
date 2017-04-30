import numpy as np
import pylab

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
    x = np.linspace(0, 50, 1000)
    y = f(x)
    pylab.plot(x, y)
    pylab.show()


def distance_travelled(t1, t2, f):
    from scipy.integrate import quad
    (int_val, err) = quad(f, t1, t2)
    return int_val


def distance_travelled_2(t1, t2, F):
    return F(t2) - F(t1)


def find_upper_bound_for_given_integral_value(inv_F, F, int_value, start_value):
    return inv_F(int_value + F(start_value))


def generate_lap_times(circumference, cutoff_speed):
    cur_time = np.random.uniform(low=0.0, high=1.0)
    abs_times = [cur_time]
    while neg_exp(cur_time) >= cutoff_speed:
        next_time = find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, circumference, cur_time)
        cur_time = next_time
        abs_times.append(cur_time)
    return abs_times


def main():
    circ = 0.85 * np.pi
    abs_times = generate_lap_times(circ, 0.5)
    print(np.diff(abs_times))
    np.testing.assert_approx_equal(distance_travelled(abs_times[0], abs_times[1], neg_exp), circ)
    plot_f(neg_exp)

    np.testing.assert_approx_equal(5.0, neg_exp_inv(neg_exp(5.0)))
    np.testing.assert_almost_equal(distance_travelled(0.5, 1, neg_exp), distance_travelled_2(0.5, 1, neg_exp_F))
    # print(find_upper_bound_for_given_integral_value(neg_exp_F_inv, neg_exp_F, 4.7581290982, 0))
    # ans = quad(neg_exp, 0, 1)
    # print(ans)


if __name__ == '__main__':
    main()
