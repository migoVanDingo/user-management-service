import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestUpdateUser(AbstractHandler):
    def __init__(self, request_id, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.payload}")

            dao_request = Request()
            update_user_response = dao_request.update(self.request_id, Constant.table['USER'], "user_id", self.payload)

            if not update_user_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DB_UPDATE --- ERROR: Failed to update user")
                raise ThrowError("Failed to update user", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_UPDATED --- RESPONSE: {update_user_response['response']}")

            if type(update_user_response['response']):
                return update_user_response

            return update_user_response['response']


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in update the user: {str(e)}", 500)