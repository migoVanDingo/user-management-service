import os
import traceback
from typing import Optional

from flask import current_app, jsonify, make_response
from pydantic import BaseModel
from api.user.handler.request_get_user import RequestGetUser
from api.user.utils.user_utils import UserUtils
from api.user_action.payload.payload_user_session import PayloadUserSession
from api.user_action.utils.user_action_utils import UserActionUtils
from classes.jwt import JWT
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request

from dotenv import load_dotenv
load_dotenv()

class IUserLogin(BaseModel):
    email: str
    password: str

class RequestUserLogin(AbstractHandler):
    def __init__(self, request_id, payload: IUserLogin):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Login")

            args = {"email": self.payload['email']}
            # Get User from Database
            get_user_response = RequestGetUser(self.request_id, args).do_process()

            # Check if user exists
            if not get_user_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- User not found")
                raise Exception("User not found")

            # Check if user is active and verified
            if not get_user_response.get('is_active'):
                raise Exception("User is not active")
            if not get_user_response.get('is_verified'):
                raise Exception("User is not verified")

            # Check if password is correct
            if not UserUtils.verify_password(self.payload['password'], get_user_response['hash']):
                raise Exception("Password is incorrect")

            # Remove sensitive data
            del get_user_response['hash']

            # Log user login
            current_app.logger.info(f"{self.request_id} --- User logged in: {get_user_response}")

            access_token, refresh_token = UserActionUtils.generate_tokens(self.request_id, get_user_response)

             # Insert refresh token in user_sessions table
            dao_request = Request()
            response = dao_request.insert(self.request_id, "user_session", PayloadUserSession.form_user_session(get_user_response['user_id'], refresh_token))

            current_app.logger.info(f"{self.request_id} --- {__class__.__name__} --- ACCESS_TOKEN: {access_token}")
            # Set refresh token in an HTTP-only secure cookie
            response = make_response(jsonify({"status": "SUCCESS", "user": get_user_response, "access_token": access_token}), 200)
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False if os.getenv("ENV") == "DEV" else True,
                max_age=60 * 60 * 24 * 7,  # 7 days expiration
                samesite="Lax" if os.getenv("ENV") == "DEV" else "Strict",
            )
            response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
            response.headers['Access-Control-Allow-Credentials'] = "true"

            return response


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {traceback.format_exc()} --- {str(e)}")
            return make_response(jsonify({"status": "FAILED", "error": str(e)}), 400)