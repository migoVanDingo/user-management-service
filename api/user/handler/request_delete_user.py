import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestDeleteUser(AbstractHandler):
    def __init__(self, request_id, user_id: str):
        self.request_id = request_id
        self.user_id = user_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.user_id}")

            dao_request = Request()
            delete_user_response = dao_request.delete(self.request_id, Constant.table['USER'], self.user_id)
            
            if not delete_user_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DELETE_USER --- ERROR: Failed to delete user")
                raise ThrowError("Failed to delete user", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DELETE_USER --- RESPONSE: {delete_user_response['response']}")

            if type(delete_user_response['response']):
                return delete_user_response
            
            return delete_user_response['response']


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in delete the user: {str(e)}", 500)