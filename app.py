import logging
import os
import uuid

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_wtf import CSRFProtect

from api.auth.auth_api import auth_api
from utility.error import ThrowError


logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                     format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://localhost:5017"])
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
csrf = CSRFProtect(app)
app.config['WTF_CSRF_ENABLED'] = False

#register blueprints
from api.user.user_api import user_api # type: ignore
from api.user_action.user_action_api import user_action_api # type: ignore
app.register_blueprint(user_api, url_prefix='/api')
app.register_blueprint(user_action_api, url_prefix='/api')
app.register_blueprint(auth_api, url_prefix='/api')


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
        response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"
        response.headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization"
        response.headers['Access-Control-Allow-Credentials'] = "true"
        return response
    else:
        request_id = str(uuid.uuid4())
        g.request_id = request_id

@app.errorhandler(ThrowError)
def handle_throw_error(error):
    response = jsonify({
        "message": str(error),
        "error_code": error.status_code
    })
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5014)