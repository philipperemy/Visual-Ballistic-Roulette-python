from Wheel import Wheel


class Measure(object):
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual


# The algorithm can be split into two parts:
# - deterministic part
# - probabilistic part
# For each part, a measure should be derived. This is the only way to calibrate it efficiently.

# Computes the angular distance between the expected number and the number
# the algorithm outputs.
# Example: metrics(32,32) = 0
# metrics(32,0) = 1 (distance of 0 to 32 is 1 on the wheel).
class AngularMeasure(Measure):
    def error(self):
        return Wheel.distance_between_numbers(int(self.expected), int(self.actual))


# Returns 1 if what the algorithm output and the expected number match
# Else returns 0.
# Example: metrics(32,12) = 1 (32 is different from 12).
# metrics(28,28) = 0
class OneHotMeasure(Measure):
    def error(self):
        return int(int(self.actual) != int(self.expected))
