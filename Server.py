#!/usr/bin/env python

import sys
import time

from flask import Flask
from flask_restful import Resource, Api, reqparse


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/utils")
    sys.path.append("./utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *
from database.SessionManager import *
from computations.predictor.physics.constantdeceleration.PredictorPhysicsConstantDeceleration import *
from computations.utils.Helper import *
from utils.Logging import *


def current_time_millis():
    return int(round(time.time() * 1000))


class Parameters(object):
    #  Request
    TIME = "ts"
    TYPE = "type"

    #  Response
    SESSION_ID = "sessionid"
    OUTCOME = "outcome"
    TYPE_WHEEL = "wheel"
    TYPE_BALL = "ball"


app = Flask(__name__)
api = Api(app)

sm = SessionManager()
da = DatabaseAccessor()
sm.init(da)


@app.after_request
def after_request(resp):
    """http://stackoverflow.com/a/28923164"""
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
    return resp


class RequestRoulette(Resource):
    @staticmethod
    def get():
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(Parameters.TIME, type=str)
            parser.add_argument(Parameters.TYPE, type=str)
            args = parser.parse_args()
            timestamp = args[Parameters.TIME]

            if timestamp is None:
                raise Exception('Parameter time ({}) missing.'.format(Parameters.TIME))
            object_type = args[Parameters.TYPE]
            if object_type is None:
                raise Exception('Parameter type ({}) missing.'.format(Parameters.TYPE))

            session_id = sm.call_manager(query_time=current_time_millis())

            if object_type == Constants.Type.BALL:
                da.insert_ball_lap_times(session_id, timestamp)
            elif object_type == Constants.Type.WHEEL:
                da.insert_wheel_lap_times(session_id, timestamp)
            else:
                raise Exception('parameter type is invalid')

            return {'status': 'success',
                    'ts': str(timestamp),
                    'type': str(object_type),
                    'session_id': str(session_id)}

        except Exception as e:
            log(e)
            return {'status': 'failure',
                    'error': str(e)}


class ResponseRoulette(Resource):
    @staticmethod
    def get():
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(Parameters.SESSION_ID, type=str)
            parser.add_argument('outcome', type=str)
            args = parser.parse_args()
            session_id = args[Parameters.SESSION_ID]
            if session_id is None:
                session_id = da.get_last_session_id()
                log('No session specified. Selecting the last known session id = {}.'.format(session_id))
            if session_id is None or session_id == '':
                log('Problem occurred. Session id should not be empty.')
                raise Exception()
            outcome = args['outcome']
            if outcome is not None and outcome != '':
                da.insert_outcome(session_id, outcome)
                log('New outcome inserted. Session id = {}, outcome = {}'.format(session_id, outcome))

            # Predict outcome workflow.
            blt = da.select_ball_lap_times(session_id)
            wlt = da.select_wheel_lap_times(session_id)
            predicted_number = PredictorPhysicsConstantDeceleration.predict_most_probable_number(blt,
                                                                                                 wlt)
            output = {'predicted_number': predicted_number,
                      'status': 'success'}
            log('Predicted number = {}, session id = {}'.format(predicted_number, session_id))
        except PositiveValueExpectedException:
            msg = 'Positive value expected.'
            log(msg)
            output = {'error': msg,
                      'status': 'failure'}
        except SessionNotReadyException:
            msg = 'Session not ready yet.'
            log(msg)
            output = {'error': msg,
                      'status': 'failure'}
        except Exception as e:
            log(e)
            output = {'error': str(e),
                      'status': 'failure'}

        return output


class HelloWorldRoulette(Resource):
    @staticmethod
    def get():
        return 'Hello Roulette world.'


api.add_resource(RequestRoulette, '/Request', methods=['GET'])
api.add_resource(ResponseRoulette, '/Response', methods=['GET'])
api.add_resource(HelloWorldRoulette, '/', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
