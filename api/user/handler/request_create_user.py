import traceback

from flask import current_app
from api.user.utils.user_utils import UserUtils
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
            password = self.payload['password']
            hash = UserUtils.hash_password(password)
            self.payload['hash'] = hash
            del self.payload['password']


            # Insert the user in the database
            dao_request = Request()
            insert_user_response = dao_request.insert(self.request_id, Constant.table['USER'], self.payload)

            # Remove hash from response
            if 'response' in insert_user_response and 'hash' in insert_user_response['response']:
                del insert_user_response['response']['hash']

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {insert_user_response}")


            return insert_user_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in create the user: {str(e)}", 500)