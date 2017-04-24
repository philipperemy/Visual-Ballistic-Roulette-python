import numpy as np


class TimeSeriesMerger(object):
    @staticmethod
    def max_len(list_of_time_series):
        return np.max([len(v) for v in list_of_time_series])

    @staticmethod
    def merge(list_of_time_series):
        """
        Merge time series from the end up to the beginning.
        The method is optimal and independent of the measurement errors.
        :param list_of_time_series: time series to aggregate together.
        :return: aggregation of all the time series.
        """
        N = TimeSeriesMerger.max_len(list_of_time_series)
        pad_time_series = []
        for time_series in list_of_time_series:
            pad_time_series.append((N - len(time_series)) * [np.nan] + list(time_series))
        return np.array(pad_time_series)

    @staticmethod
    def compute_loss(time_series, list_of_time_series):
        loss = 0.0
        for element in list_of_time_series:
            loss += np.sum((np.array(time_series - element) ** 2) * np.array(time_series != 0, dtype=bool))
        return loss

    @staticmethod
    def optimal_roll(list_of_time_series):
        """
        Used when the end of the time series do not coincide. Example is:
        [[1, 20, 30, 4], [20, 30, 4], [30, 4], [20, 30]]
        This method is not optimal and heavily depends on the measurement errors.
        :param list_of_time_series: time series to match together.
        :return: best placement of the time series.
        """
        list_of_time_series = TimeSeriesMerger.merge(list_of_time_series)
        N = TimeSeriesMerger.max_len(list_of_time_series)
        best_time_series_combination = list()

        # TODO: monte carlo to select the most stable solution.
        # Helper.shuffle(list_of_time_series)
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
        """INPUT1 time_series1 = [1, 2, 3, 4]
           INPUT2 time_series2 = [0, 0, 0, 0, 1, 2, 3, 3, 0, 0, 0, 0]
           OUTPUT fit_time_series_1 = [0, 0, 0, 0, 1, 2, 3, 4, 0, 0, 0, 0], index = 4
        """
        N = len(time_series2)
        time_series = (N - len(time_series1)) * [0] + list(time_series1)
        losses = np.zeros(N)
        for i in range(N):
            losses[i] = TimeSeriesMerger.compute_loss(np.roll(time_series, -i), [time_series2])
        time_series_fit = np.roll(time_series, -losses.argmin())
        return time_series_fit, np.where(time_series_fit > 0)[0][0]

    @staticmethod
    def find_nearest_neighbors(time_series1, list_of_time_series, index_of_start, neighbors_count):
        a = list_of_time_series[:, index_of_start:index_of_start + len(time_series1)]
        b = a[~np.isnan(a).any(axis=1)]
        losses = np.square(time_series1 - b)
        losses = np.sum(losses, axis=1)
        matched_game_indices = np.argsort(losses)[:neighbors_count]
        return matched_game_indices


if __name__ == '__main__':
    a = np.array([3, 2, 1, 1, 2, 0, 0, 4])
    print(a[np.argsort(a)[:2]])
