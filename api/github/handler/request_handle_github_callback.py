import os
from flask import current_app, jsonify, make_response, redirect, session
import requests
from api.github.handler.request_fetch_github_user import RequestFetchGithubUser
from api.github.handler.request_fetch_github_user_emails import RequestFetchGithubUserEmails
from api.user.handler.request_get_user import RequestGetUser
from api.user_action.handler.request_register_user import RequestRegisterUser
from api.user_action.payload.payload_register import PayloadRegister
from api.user_action.payload.payload_user_session import PayloadUserSession
from api.user_action.utils.user_action_utils import UserActionUtils
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.request import Request


class RequestHandleGithubCallback(AbstractHandler):
    def __init__(self, request_id, code, flow_type):
        self.request_id = request_id
        self.code = code
        self.flow_type = flow_type

    def do_process(self):
        try:
            # Exchange code for an access token
            token_url = "https://github.com/login/oauth/access_token"
            headers = {"Accept": "application/json"}
            payload = {
                "client_id": Constant.GITHUB_CLIENT_ID,
                "client_secret": Constant.GITHUB_CLIENT_SECRET,
                "code": self.code,
                "redirect_uri": Constant.GITHUB_REDIRECT_URI,
            }
            response = requests.post(token_url, headers=headers, data=payload)
            data = response.json()

            if "access_token" not in data:
                return jsonify({"error": "Failed to retrieve access token"}), 400

            access_token = data["access_token"]
            

            # Request fetch user profile
            request = RequestFetchGithubUser(self.request_id, access_token)
            github_user = request.do_process()

            # Get User Email
            email_request = RequestFetchGithubUserEmails(
                self.request_id, access_token)
            email = email_request.do_process()

            if email:
                github_user["email"] = email
            else:
                current_app.logger.error(
                    f"{self.request_id} --- GITHUB_CALLBACK: Failed to fetch email")

            if self.flow_type == "signup":
                current_app.logger.info(
                    f"{self.request_id} --- GITHUB_CALLBACK: signup -- user: {github_user}")
                return self._register_user(github_user)

            elif self.flow_type == "login":
                current_app.logger.info(
                    f"{self.request_id} --- GITHUB_CALLBACK: login -- user: {github_user}")
                github_token = access_token
                return self._login_user(github_user, github_token)

        except Exception as e:
            current_app.logger.error(
                f"{self.request_id} --- {self.__class__.__name__} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}

    def _register_user(self, github_user):
        # Create new user payload
        register_payload = PayloadRegister.form_register_payload(
            {"username": github_user["login"], "email": github_user["email"], "github_id": github_user["id"], "user_type": "github", "avatar_url": github_user["avatar_url"]})
        
        current_app.logger.info(
            f"{self.request_id} --- GITHUB_CALLBACK: Registering user: {register_payload}")

        # Create Job to Register User
        api_request = RequestRegisterUser(self.request_id, register_payload)
        response = api_request.do_process()
        return make_response(redirect("http://localhost:5173/login"))

    def _login_user(self, github_user, github_token):
        email = github_user["email"]

        # Get user
        dao_request = RequestGetUser(self.request_id, {"email": email})
        user_response = dao_request.do_process()
        access_token, refresh_token = UserActionUtils.generate_tokens(
            self.request_id, user_response)
        dao_request = Request()
        response = dao_request.insert(self.request_id, "user_session", PayloadUserSession.form_user_session(user_response["user_id"], refresh_token))
        current_app.logger.info(
            f"{self.request_id} --- {__class__.__name__} --- ACCESS_TOKEN: {access_token} --- REFRESH_TOKEN: {refresh_token}")
        response = make_response(redirect(f"http://localhost:5173/handler/login?user_id={user_response['user_id']}"))
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False if os.getenv("ENV") == "DEV" else True,
            max_age=60 * 60 * 24 * 7,  # 7 days expiration
            samesite="Lax" if os.getenv("ENV") == "DEV" else "Strict",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False if os.getenv("ENV") == "DEV" else True,
            max_age=60 * 60 * 24 * 7,  # 7 days expiration
            samesite="Lax" if os.getenv("ENV") == "DEV" else "Strict",
        )

        response.set_cookie(
            key="github_token",
            value=github_token,
            httponly=True,
            secure=False if os.getenv("ENV") == "DEV" else True,
            max_age=60 * 60 * 8,  # 7 days expiration
            samesite="Lax" if os.getenv("ENV") == "DEV" else "Strict",
        )
        

        return response
