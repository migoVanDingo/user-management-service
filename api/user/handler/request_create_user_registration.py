
from datetime import datetime, timedelta
import traceback

from flask import current_app
from api.user.utils.user_utils import UserUtils
from classes.jwt import JWT
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.request import Request


class RequestCreateUserRegistration(AbstractHandler):
    def __init__(self, request_id: str, user_id: str):
        self.request_id = request_id
        self.user_id = user_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- USER_ID: {self.user_id}")

            verify_token = UserUtils.generate_plaintext_token()
            hash = UserUtils.hash_password(verify_token)

            date_time, timestamp = self.generate_expiration_timestamp()


            dao_request = Request()
            insert_user_register_response = dao_request.insert(self.request_id, Constant.table['USER_REGISTRATION'], {"user_id": self.user_id, "hash": hash, "exp_datetime": date_time, "exp_timestamp": timestamp})

            if "response" not in insert_user_register_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_USER_REGISTRATION --- ERROR: Failed to create user registration")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} --- Failed to create user registration")
            
            #Insert user role
            insert_user_role_response = dao_request.insert(self.request_id, Constant.table['USER_ROLES'], {"user_id": self.user_id, "role": "DEVELOPER", "level": 100, "created_by": "SYSTEM"})

            if "response" not in insert_user_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_USER_REGISTRATION --- ERROR: Failed to create user role")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} --- Failed to create user role")
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_USER_REGISTRATION --- COMPLETE")

            #Embed user_id and token in account_token for email verification
            jwt = JWT()
            account_token = jwt.account_token({"user_id": self.user_id, "token": verify_token})

            return {"status": "SUCCESS", "message": "User registration created successfully", "data":{ "user_registration_id": insert_user_register_response['response']['user_registration_id'] , "token": account_token}}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}
        

    def generate_expiration_timestamp(self):
        expiration_time = datetime.now() + timedelta(hours=24)
        date_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S") 
        timestamp = int(expiration_time.timestamp()) 
        return date_time, timestamp