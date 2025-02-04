from datetime import datetime
import traceback

from flask import current_app
from api.user.utils.user_utils import UserUtils
from classes.jwt import JWT
from interface.abstract_handler import AbstractHandler
from utility.request import Request


class RequestVerifyUserAccount(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- VERIFY_USER_ACCOUNT")

            jwt = JWT()

            jwt_token = self.payload.get("token")
            decode_jwt = jwt.decode_token(jwt_token)
            token = decode_jwt["token"]
            user_id = decode_jwt["user_id"]

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- USER_ID: {user_id} --- TOKEN: {token}")
            

            # Get user registration
            dao_request = Request()
            user_registration = dao_request.read(self.request_id, "user_registration", {"user_id": user_id, "is_active": 1})

            if "response" not in user_registration or not user_registration['response']:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ERROR: Failed to get user registration")
                raise Exception(f"Failed to get user registration")
            
            user_registration = user_registration['response']

            # Gen epoch and compare to exp_timestamp
            if user_registration['exp_timestamp'] < datetime.now().timestamp():
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ERROR: User registration expired")
                raise Exception(f"User registration expired")

            # Compare the tokens
            if not UserUtils.verify_password(token, user_registration['hash']):
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ERROR: User verification failed")
                raise Exception(f"User verification failed")
            
            dao_request.update(self.request_id, "user_registration", "user_registration_id", user_registration['user_registration_id'], {"is_active": 0})
            
            
            # Update user set is_verified = 1
            dao_request.update(self.request_id, "user", "user_id", user_id, {"is_verified": 1})
        
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- User verified")
            return {"status": "SUCCESS", "message": "User verified"}

            
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}