#!/usr/bin/env python

import sys
import time

from flask import Flask
from flask_restful import Resource, Api, reqparse


def add_all_folders_to_python_path():
    sys.path.append("./database")
    sys.path.append("./computations")
    sys.path.append("./computations/comp_utils")
    sys.path.append("./comp_utils")


add_all_folders_to_python_path()

from database.DatabaseAccessor import *
from database.SessionManager import *
from PredictorPhysics import *
from utils.Logging import *


def current_time_millis():
    return int(round(time.time() * 1000))


class Parameters(object):
    #  Request
    TIME = 'ts'
    TYPE = 'type'

    #  Response
    SESSION_ID = 'sessionid'
    OUTCOME = 'outcome'
    TYPE_WHEEL = 'wheel'
    TYPE_BALL = 'ball'


app = Flask(__name__)
api = Api(app)

da = DatabaseAccessor.get_instance()
sm = SessionManager(da)
PredictorPhysics.load_cache(da)


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
            start_time = current_time_millis()
            parser = reqparse.RequestParser()
            parser.add_argument(Parameters.SESSION_ID, type=str)
            parser.add_argument(Parameters.OUTCOME, type=str)
            args = parser.parse_args()
            session_id = args[Parameters.SESSION_ID]
            if session_id is None:
                session_id = da.get_last_session_id()
                log('No session specified. Selecting the last known session id = {}.'.format(session_id))
            if session_id is None or session_id == '':
                log('Problem occurred. Session id should not be empty.')
                raise Exception()
            outcome = args[Parameters.OUTCOME]
            if outcome is not None and outcome != '':
                # Insert number workflow
                da.insert_outcome(session_id, 0, outcome)
                log('New outcome inserted. Session id = {}, outcome = {}'.format(session_id, outcome))
                return {'status': 'success',
                        'outcome': outcome,
                        'session_id': session_id}

            # Predict number workflow.
            ball_recorded_times = da.select_ball_recorded_times(session_id)
            wheel_recorded_times = da.select_wheel_recorded_times(session_id)
            _, predicted_number = PredictorPhysics.predict_most_probable_number(ball_recorded_times,
                                                                                wheel_recorded_times)
            log('Predicted number = {}, session id = {}'.format(predicted_number, session_id))
            return {'status': 'success',
                    'predicted_number': predicted_number,
                    'latency_ms': current_time_millis() - start_time}
        except Exception as e:
            log(e)
            return {'status': 'failure',
                    'error': str(e)}


class HelloWorldRoulette(Resource):
    @staticmethod
    def get():
        return 'Hello Roulette world. Hit /Request or /Response.'


api.add_resource(RequestRoulette, '/Request', methods=['GET'])
api.add_resource(ResponseRoulette, '/Response', methods=['GET'])
api.add_resource(HelloWorldRoulette, '/', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
