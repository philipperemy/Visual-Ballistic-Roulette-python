from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Predictor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init(self, da):
        """ generated source for method init """

    @abstractmethod
    def predict(self, ball_lap_times, wheel_lap_times):
        """ generated source for method predict """

    @abstractmethod
    def clear(self):
        """ generated source for method clear """
