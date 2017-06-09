from uuid import uuid4
from flask import request, Response, jsonify
import database.user
import utils
from .exceptions import InvalidRequest, AuthFailed

import jwt


def login():
    try:
        request_data = request.get_json()
        if request_data is None:
            raise InvalidRequest()

        username = request_data.get('username')
        password = request_data.get('password')
        old_token = request_data.get('token')

        if username is not None and password is not None:
            if database.user.is_valid(username, password):
                timestamp_now = utils.utc_timestamp()
                return jsonify({'token': new_token(timestamp_now)})
            else:
                raise AuthFailed()
        elif old_token is not None:
            payload = utils.jwt_decode(old_token)
            timestamp_now = utils.utc_timestamp()
            if payload['exp'] < timestamp_now:
                raise AuthFailed()
            return jsonify({'token': new_token(timestamp_now)})
        else:
            raise InvalidRequest()
    except InvalidRequest:
        return Response(status=400)
    except (jwt.DecodeError, AuthFailed):
        return Response(status=401)

def new_token(time_stamp):
    return utils.jwt_encode({
        'iss': 'dispatcher-backend',
        'exp': time_stamp + 60 * 30,
        'iat': time_stamp,
        'jti': str(uuid4()),
        'scope': ['dashboard', 'tasks']
    })