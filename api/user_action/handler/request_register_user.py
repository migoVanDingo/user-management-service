
import random
import string
import traceback
import bleach

from flask import current_app, json
import requests
from api.user_action.payload.payload_register import PayloadRegister
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.registration_form import RegistrationForm


class RequestRegisterUser(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Request payload: {self.payload}")
            # form = RegistrationForm(data=self.payload)
            # if not form.validate():
            #     current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Payload Validation Error: {form.errors}")
            #     return {"status": "FAILED", "error": form.errors}
            
            self.payload['user_id'] = self.generate_temp_user_id()
            
            # Form Create Job Payload
            data =  PayloadRegister.form_register_payload(self.payload)

            response = requests.post(Constant.base_url + Constant.services["JOB"]["PORT"] + Constant.services["JOB"]["ENDPOINT"]["CREATE-JOB"], json=data)

            print(f"Response: {response}")
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Response: {response.json()}")
            response = response.json()

            if "status" not in response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Job creation failed")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} --- Job creation failed. User could not be registered")

            return {"status": "SUCCESS", "data": response['job_id']}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}

    def generate_temp_user_id(self):
        prefix = "TEMP"
        N = 25
        id = prefix + ''.join(random.choices(string.digits, k= N - len(prefix) - 20)) +''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        return id
    
    def sanitize_input(input_data):
        """Sanitize input using bleach."""
        return bleach.clean(input_data, tags=[], strip=True)