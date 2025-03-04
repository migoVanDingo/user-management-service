import traceback

from flask import current_app
from api.user.payload.payload_user import PayloadUser
from api.user.utils.user_utils import UserUtils
from api.user.handler.request_create_user_registration import RequestCreateUserRegistration
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestCreateUser(AbstractHandler):
    def __init__(self, request_id, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.payload}")

            # Hash password and remove it from payload
            if "password" in self.payload:
                password = self.payload['password']
                hash = UserUtils.hash_password(password)
                self.payload['hash'] = hash
                del self.payload['password']


            # Insert the user in the database
            dao_request = Request()
            insert_user_response = dao_request.insert(self.request_id, Constant.table['USER'], PayloadUser.form_user_payload(self.payload))


            if "response" not in insert_user_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ERROR: Failed to create user")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} --- Failed to create user")
            
            # Form response payload removing hash and password
            response = PayloadUser.form_user_response(insert_user_response['response'])

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {response}")


            return { "status": "SUCCESS", "data": response }

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}