import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetUser(AbstractHandler):
    def __init__(self, request_id, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.args}")

            dao_request = Request()
            get_user_response = dao_request.read(self.request_id, Constant.table["USER"], self.args)

            if not get_user_response or not get_user_response['response']:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- User not found")
                raise ThrowError(f"User not found", 404)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {get_user_response}")

            # Remove hash from response
            del get_user_response['response']['hash']
            
            return get_user_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in get the user: {str(e)}", 500)