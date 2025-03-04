from flask import current_app
from interface.abstract_handler import AbstractHandler


class RequestSignupWithGithub(AbstractHandler):
    def __init__(self, request_id):
        self.request_id = request_id

    def do_process(self):
        try:
            pass
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}