from pydantic import BaseModel

class IInsertUser(BaseModel):
    username: str
    hash: str
    email: str

class PayloadUser:
    @staticmethod
    def form_user_payload(data:dict) -> IInsertUser:
        return {
            "username": data.get("username"),
            "hash": data.get("hash"),
            "email": data.get("email")
        }