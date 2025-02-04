class PayloadRegister:
    @staticmethod
    def form_register_payload(data: dict):
        payload = {
            "username": data.get("username"),
            "email": data.get("email"),
            "password": data.get("password"),
            "user_id": data.get("user_id"),
            "job_name": "REGISTER_USER",
  
        }

        if "ip" in data:
            payload["ip"] = data.get("ip")
        
        return payload