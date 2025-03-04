from flask import Blueprint, current_app, json, jsonify, request

from classes.jwt import JWT


auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/auth/refresh-token', methods=['POST'])
def refresh_access_token():
    current_app.logger.info(f"========= REFRESH_TOKEN =========")
    data = json.loads(request.data)
    refresh_token = data['refresh_token']
    jwt = JWT()
    response = jwt.refresh_access_token(refresh_token)

    return response


# Decode token
@auth_api.route('/auth/decode-token', methods=['POST'])
def decode_token():
    current_app.logger.info(f"========= DECODE_TOKEN =========")
    data = json.loads(request.data)
    token = data['token']
    jwt = JWT()
    response = jwt.decode_token(token)

    return response

@auth_api.route("/auth/access_token", methods=["GET"])
def get_access_token():
    access_token = request.cookies.get("access_token")

    if not access_token:
        return jsonify({"error": "Access token not found"}), 401

    return jsonify({"access_token": access_token})
