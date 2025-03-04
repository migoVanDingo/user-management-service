class PayloadRegister:
    @staticmethod
    def form_register_payload(data: dict):
        payload = {
            "username": data.get("username"),
            "email": data.get("email"),
            "user_id": data.get("user_id"),
            "user_type": data.get("user_type"),
            "job_name": "REGISTER_USER",
  
        }

        if "github_id" in data: 
            payload["github_id"] = data.get("github_id")

        if "password" in data:
            payload["password"] = data.get("password")

        if "ip" in data:
            payload["ip"] = data.get("ip")
        
        return payload