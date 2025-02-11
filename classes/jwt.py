import datetime
import os
import traceback

from flask import current_app, jsonify
import jwt

from dotenv import load_dotenv


class JWT:
    def __init__(self):
        load_dotenv()
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        if not self.secret_key:
            raise Exception("SECRET_KEY not found in environment variables")

    def decode_token(self, token):
        try:
            decode_payload = jwt.decode(
                token, self.secret_key, algorithms=["HS256"])
            return decode_payload
        except jwt.ExpiredSignatureError:
            current_app.logger.error(f"Token has expired")
            return {"status": "FAILED", "error": "Token has expired"}
        except jwt.InvalidTokenError:
            current_app.logger.error(f"Invalid token")
            return {"status": "FAILED", "error": "Invalid token"}
        except Exception as e:
            current_app.logger.error(
                f"{self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
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
            current_app.logger.error(
                f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "message": str(e)}, 500

    def account_token(self, payload: dict):
        try:
            now = datetime.datetime.now(datetime.timezone.utc)

            account_token_payload = {}
            account_token_payload["exp"] = now + datetime.timedelta(hours=24)
            for key, value in payload.items():
                account_token_payload[key] = value

            account_token = jwt.encode(
                account_token_payload,
                self.secret_key,
                algorithm="HS256",
            )

            return account_token

        except Exception as e:
            current_app.logger.error(
                f"{self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "message": str(e)}, 500

    def refresh_access_token(self, refresh_token):
        try:
            """Endpoint to refresh the access token using a valid refresh token."""
            

            if not refresh_token:
                return jsonify({"message": "Refresh token is missing!"}), 400

            # Decode the refresh token to get the user info and check validity
            decoded_refresh_token = self.decode_token(refresh_token)
            if not decoded_refresh_token:
                return jsonify({"message": "Invalid or expired refresh token!"}), 401

            # Generate a new access token (This example generates a JWT as an access token)
            # Example: Get the user ID or other data from the decoded refresh token
            user_id = decoded_refresh_token["sub"]

            # Generate new access token with a short expiry time
            access_token = jwt.encode({
                "sub": user_id,
                # Example: Set a 15-minute expiry for the access token
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
            }, self.secret_key, algorithm="HS256")
            current_app.logger.info(f"ACCESS_TOKEN_REFRESHED: {access_token}")
            return jsonify({
                "access_token": access_token
            })
        except Exception as e:
            current_app.logger.error(
                f"{self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "message": str(e)}, 500
