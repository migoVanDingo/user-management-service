import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestGetUserList(AbstractHandler):
    def __init__(self, request_id, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- ARGS: {self.args}")

            dao_request = Request()
            get_list_response = dao_request.read_list(self.request_id, "datastore", self.args)

            if not get_list_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE --- ERROR: Failed to get datastore")
                raise ThrowError("Failed to get datastore", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_LIST --- RESPONSE: {get_list_response['response']}")

            for item in get_list_response['response']:
                del item['hash']

            return get_list_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"There was a problem in get the user list: {str(e)}", 500)