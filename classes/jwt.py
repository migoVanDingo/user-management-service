import datetime
import traceback

from flask import current_app
import jwt


class JWT:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def decode_token(self, token):
        try:
            decode_payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return decode_payload
        except jwt.ExpiredSignatureError:
            current_app.logger.error(f"Token has expired")
            return {"status": "FAILED", "error": "Token has expired"}
        except jwt.InvalidTokenError:
            current_app.logger.error(f"Invalid token")
            return {"status": "FAILED", "error": "Invalid token"}
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}

    def generate_tokens(self, user_id: str, role: str):
        try:

            now = datetime.datetime.now(datetime.timezone.utc)
            access_token_payload = {
                "sub": user_id,
                "role": role,
                "exp": now + datetime.timedelta(minutes=15),
                "iat": now,
                "nbf": now,
            }

            access_token = jwt.encode(
                access_token_payload,
                self.secret_key,
                algorithm="HS256",
            )

            refresh_token_payload = {
                "sub": user_id,
                "role": role,
                "exp": now + datetime.timedelta(days=7),
                "iat": now,
                "nbf": now,
            }

            refresh_token = jwt.encode(
                refresh_token_payload,
                self.secret_key,
                algorithm="HS256",
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "message": str(e)}, 500