from computations.predictor.physics.constantdeceleration.PredictorPhysicsConstantDeceleration import *

if __name__ == '__main__':
    blt = []
    wlt = []
    n_predicted = PredictorPhysicsConstantDeceleration.predict_most_probable_number(blt, wlt, debug=False)
