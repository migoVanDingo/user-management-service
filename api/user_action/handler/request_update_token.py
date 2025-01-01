import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError

class RequestUpdateToken(AbstractHandler):
    def __init__(self, request_id, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- NOT IMPLEMENTED")
            raise NotImplementedError

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in update token: {str(e)}", 500)