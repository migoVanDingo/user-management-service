from flask import current_app, jsonify, session
import requests
from interface.abstract_handler import AbstractHandler


class RequestFetchGithubUser(AbstractHandler):
    def __init__(self, request_id, access_token):
        self.request_id = request_id
        self.access_token = access_token

    def do_process(self):
        try:
            
            if not self.access_token:
                return jsonify({"error": "Unauthorized"}), 401

            user_url = "https://api.github.com/user"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(user_url, headers=headers)

            return response.json()
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}