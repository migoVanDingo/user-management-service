import os
from flask import current_app, jsonify, make_response
from api.user_action.payload.payload_user_session import PayloadUserSession
from classes.jwt import JWT
from utility.request import Request


class UserActionUtils:
    @staticmethod
    def generate_tokens(request_id, user):

            # Fetch user role
            dao_request = Request()
            user_role = dao_request.read(request_id, "user_roles", {"user_id": user['user_id']})['response']

            # Generate tokens
            jwt = JWT()
            tokens = jwt.generate_tokens(user['user_id'], user_role['role'])

            access_token = tokens['access_token']
            refresh_token = tokens['refresh_token']

            return access_token, refresh_token

           
    