from pydantic import BaseModel

class IInsertUser(BaseModel):
    username: str
    hash: str
    email: str

class PayloadUser:
    @staticmethod
    def form_user_payload(data:dict) -> IInsertUser:
        payload =  {
            "username": data.get("username"),
            "email": data.get("email"),
            "user_type": data.get("user_type")
        }
        if "hash" in data:
            payload["hash"] = data.get("hash")

        if "github_id" in data:
            payload["github_id"] = data.get("github_id")

        return payload

        

    
    @staticmethod
    def form_user_response(data:dict) -> dict:
        return {
            "user_id": data.get("user_id"),
            "username": data.get("username"),
            "email": data.get("email")
        }