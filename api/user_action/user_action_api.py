from flask import Blueprint, g, json, request

from api.user_action.handler.request_user_login import RequestUserLogin

user_action_api = Blueprint('user_action_api', __name__)

# User login
@user_action_api.route('/user/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    request_id = g.request_id
    api_request = RequestUserLogin(request_id, data)
    response = api_request.do_process()
    return response

# User logout
@user_action_api.route('/user/logout', methods=['POST'])
def logout():
    return "Not implemented"

# User registration
@user_action_api.route('/user/register', methods=['POST'])
def register():
    return "Not implemented"

# User update
@user_action_api.route('/user', methods=['PUT'])
def update_user():
    return "Not implemented"

# User delete
@user_action_api.route('/user', methods=['DELETE'])
def delete_user():
    return "Not implemented"