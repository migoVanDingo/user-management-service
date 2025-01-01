import traceback
from typing import Optional

from flask import current_app
from pydantic import BaseModel
from api.user.handler.request_get_user import RequestGetUser
from api.user.utils.user_utils import UserUtils
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request

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

            args = {
                "email": self.payload['email']
            }

            # Get User from Database
            get_user_response = RequestGetUser(self.request_id, args).do_process()

            # Check if user exists
            if not get_user_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- User not found")
                raise ThrowError("User not found", 404)

            # Check if user is active
            if not get_user_response['is_active']:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- User is not active")
                raise ThrowError("User is not active", 400)
            
            # Check if user is verified
            # if not get_user_response['is_verified']:
            #     current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- User is not verified")
            #     raise ThrowError("User is not verified", 400)
            
            # Check if password is correct
            if not UserUtils.verify_password(self.payload['password'], get_user_response['hash']):
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Password is incorrect")
                raise ThrowError("Password is incorrect", 400)


            # Remove hash from response
            del get_user_response['hash']

            # Log user login
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- User logged in: {get_user_response}")

            return get_user_response

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in login the user: {str(e)}", 500)