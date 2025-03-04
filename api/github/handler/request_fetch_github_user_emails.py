from flask import current_app
from api.github.utils.github_utility import GithubUtility
from interface.abstract_handler import AbstractHandler


class RequestFetchGithubUserEmails(AbstractHandler):
    def __init__(self, request_id, access_token):
        self.request_id = request_id
        self.access_token = access_token

    def do_process(self):
        try:
            return GithubUtility.fetch_github_email(self.access_token)
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}