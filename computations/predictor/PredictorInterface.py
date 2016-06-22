from __future__ import print_function

from PredictorPhysicsConstantDeceleration import PredictorPhysicsConstantDeceleration


class PredictorInterface(object):
    predictor_physics_constant_deceleration = PredictorPhysicsConstantDeceleration()

    @staticmethod
    def get_instance(cls):
        """ generated source for method get_instance """
        if cls.instance_ is None:
            cls.instance_ = PredictorInterface()
        return cls.instance_

    def physics_constant_deceleration(self):
        """ generated source for method physics_constantDeceleration """
        return self.predictor_physics_constant_deceleration
