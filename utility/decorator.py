from flask import request, jsonify
from functools import wraps
from jwt import decode, ExpiredSignatureError, InvalidTokenError


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check the 'Authorization' header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            decoded_token = decode(token, "your_secret_key", algorithms=["HS256"])
            # You can access user info from decoded_token["sub"], etc.
        except ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated

