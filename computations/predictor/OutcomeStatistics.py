import collections

from Wheel import *


class OutcomeStatistics(object):
    # 	 * Statistics of a list of numbers. Example is: if we have two numbers 0, 32
    # 	 * and 15. mean(0,32,15) = 32 because on the wheel, they are sorted. Also we
    # 	 * can compute the variance. If all the numbers are very close one another,
    # 	 * the variance will be low and the prediction be accurate.
    @staticmethod
    def create(outcome_numbers):
        counter = collections.Counter(outcome_numbers)

        #  Reduce the Residuals Sum of Squares (RSS).
        rss_list = np.zeros(len(Wheel.NUMBERS))
        for idx_mean in range(len(Wheel.NUMBERS)):
            rss = 0.0
            for outcome in outcome_numbers:
                rss += Wheel.distance_between_numbers(outcome, Wheel.NUMBERS[idx_mean]) ** 2
            rss_list[idx_mean] = rss
        mean_number = Wheel.NUMBERS[rss_list.argmin()]

        variance = 0.0
        for outcome in outcome_numbers:
            variance += Wheel.distance_between_numbers(outcome, mean_number) ** 2

        most_probable_number = counter.most_common()

        if most_probable_number is None:
            raise (Exception('Most probable number should not be null'))

        return {'mean_number': mean_number,
                'std_deviation': np.sqrt(variance),
                'most_common': most_probable_number}
