from flask import Blueprint, g, json, request

from api.user.handler.request_create_user import RequestCreateUser
from api.user.handler.request_delete_user import RequestDeleteUser
from api.user.handler.request_get_user import RequestGetUser
from api.user.handler.request_get_user_list import RequestGetUserList
from api.user.handler.request_update_user import RequestUpdateUser


user_api = Blueprint('user_api', __name__)

# Create user
@user_api.route('/user', methods=['POST'])
def create_user():
    data = json.loads(request.data)
    request_id = g.request_id
    api_request = RequestCreateUser(request_id, data)
    response = api_request.do_process()
    return response

# Read user
@user_api.route('/user', methods=['GET'])
def get_user():
    args = request.args
    request_id = g.request_id
    api_request = RequestGetUser(request_id, args)
    response = api_request.do_process()
    return response


# Get user list
@user_api.route('/user/list', methods=['GET'])
def get_user_list():
    args = request.args
    request_id = g.request_id
    api_request = RequestGetUserList(request_id, args)
    response = api_request.do_process()
    return response

# Update user
@user_api.route('/user', methods=['PUT'])
def update_user():
    data = json.loads(request.data)
    request_id = g.request_id
    api_request = RequestUpdateUser(request_id, data)
    response = api_request.do_process()
    return response


# Delete user
@user_api.route('/user/<string:id>', methods=['DELETE'])
def delete_user(id):
    request_id = g.request_id
    api_request = RequestDeleteUser(request_id, id)
    response = api_request.do_process()
    return response



