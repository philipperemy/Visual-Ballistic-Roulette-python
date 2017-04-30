from pprint import pprint
from time import sleep

from computations.Wheel import Wheel
from simulations.data_generation_5_b_w import next_batch
from simulations.nn.classifier_model_definition import *
from simulations.nn.numbers_to_categories import NumbersToCategorical


def main():
    num_to_cat = NumbersToCategorical(['N_{}'.format(v) for v in Wheel.NUMBERS])

    time_len = 10
    m = get_model(time_len=time_len, num_classes=len(Wheel.NUMBERS))
    build_model(m)
    while True:
        nb = next_batch(debug=False)
        nums = np.array([num_to_cat.get_one_hot_vector('N_{}'.format(v)) for v in nb['numbers']])
        y = num_to_cat.get_one_hot_vector('N_{}'.format(nb['number_cutoff']))
        lap_times = np.insert(nb['lap_times'], 0, [0])
        kx_train = [np.expand_dims(nums[-time_len:], axis=0), np.expand_dims(lap_times[-time_len:], axis=0)]
        ky_train = y

        fit_model(m, kx_train, np.expand_dims(ky_train, axis=0), max_epochs=1)
        # print('-' * 80)
        # pprint(nb)


if __name__ == '__main__':
    main()
