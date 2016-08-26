from Helper import *


class TimeSeriesMerger(object):
    @staticmethod
    def max_len(list_of_time_series):
        return np.max([len(v) for v in list_of_time_series])

    @staticmethod
    def merge(list_of_time_series):
        N = TimeSeriesMerger.max_len(list_of_time_series)
        pad_time_series = []
        for time_series in list_of_time_series:
            pad_time_series.append((N - len(time_series)) * [np.nan] + list(time_series))
        return pad_time_series

    @staticmethod
    def compute_loss(time_series, list_of_time_series):
        loss = 0.0
        for element in list_of_time_series:
            loss += np.sum((np.array(time_series - element) ** 2) * np.array(time_series != 0, dtype=bool))
        return loss

    @staticmethod
    def optimal_roll(list_of_time_series):
        list_of_time_series = TimeSeriesMerger.merge(list_of_time_series)
        N = TimeSeriesMerger.max_len(list_of_time_series)
        best_time_series_combination = list()
        for time_series in list_of_time_series:
            if len(best_time_series_combination) == 0:
                best_time_series_combination.append(time_series)
            else:
                losses = np.zeros(N)
                for i in range(N):
                    losses[i] = TimeSeriesMerger.compute_loss(np.roll(time_series, -i), list_of_time_series)
                optimal_roll_time_series = np.roll(time_series, -losses.argmin())
                best_time_series_combination.append(optimal_roll_time_series)
        return np.array(best_time_series_combination)

    @staticmethod
    def find_index(time_series1, time_series2):
        N = len(time_series2)
        time_series = (N - len(time_series1)) * [0] + list(time_series1)
        losses = np.zeros(N)
        for i in range(N):
            losses[i] = TimeSeriesMerger.compute_loss(np.roll(time_series, -i), [time_series2])
        return np.roll(time_series, -losses.argmin())


if __name__ == '__main__':
    lts = [[1, 20, 30, 4], [20, 30, 4], [30, 4], [20, 30]]
    print(lts)
    merged_lts = TimeSeriesMerger.optimal_roll(lts)
    print(merged_lts)
    print(np.mean(merged_lts, axis=0))

    l1 = [1, 2, 3, 4]
    l2 = [0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0]

    a = TimeSeriesMerger.find_index(l1, l2)
    print(a)
    print(np.where(a > 0)[0][0])
