from keras.utils.np_utils import to_categorical
from natsort import natsorted


class NumbersToCategorical:
    def __init__(self, data):
        self.number_ids = natsorted(list(data))
        int_number_ids = list(range(len(self.number_ids)))
        self.map_numbers_to_index = dict([(k, v) for (k, v) in zip(self.number_ids, int_number_ids)])
        self.map_index_to_numbers = dict([(v, k) for (k, v) in zip(self.number_ids, int_number_ids)])
        self.number_categories = to_categorical(int_number_ids, num_classes=len(self.number_ids))

    def get_number_from_index(self, index):
        return self.map_index_to_numbers[index]

    def get_one_hot_vector(self, number_id):
        index = self.map_numbers_to_index[number_id]
        return self.number_categories[index]

    def get_number_ids(self):
        return self.number_ids
