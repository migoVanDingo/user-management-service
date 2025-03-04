import os
from flask import Blueprint, current_app, g, jsonify, redirect, request, session
from dotenv import load_dotenv
import requests

from api.github.handler.request_handle_github_callback import RequestHandleGithubCallback
from api.github.utils.github_utility import GithubUtility
from utility.constant import Constant
load_dotenv()

github_api = Blueprint('github_api', __name__)


@github_api.route('/github/signup', methods=['GET'])
def github_signup():
    """Redirects user to GitHub OAuth page."""
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- GITHUB_SIGNUP: Redirecting to GitHub OAuth page")
    return GithubUtility.github_oauth("signup")


@github_api.route('/github/login', methods=['GET'])
def github_login():
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- GITHUB_LOGIN: Redirecting to GitHub OAuth page")
    return GithubUtility.github_oauth("login")


@github_api.route("/github/callback")
def github_callback():
    """Handles GitHub OAuth callback."""
    code = request.args.get("code")
    state = request.args.get("state")
    if not code:
        return jsonify({"error": "Authorization failed"}), 400
    
    request_id = g.request_id
    
    verify, flow_type = GithubUtility.verify_oauth_state(state)
    if not verify:
        current_app.logger.error(f"{request_id} --- GITHUB_CALLBACK: Invalid state token")
        
    
    api_request = RequestHandleGithubCallback(request_id, code, flow_type)
    return api_request.do_process()


    



@github_api.route("/github/user")
def github_user():
    """Fetch authenticated user profile."""
    access_token = session.get("github_token")
    if not access_token:
        return jsonify({"error": "Unauthorized"}), 401

    user_url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_url, headers=headers)

    return jsonify(response.json())


@github_api.route("/github/repos")
def github_repos():
    """Fetch user's repositories."""

    current_app.logger.info(f"Fetching user's Github repositories")
    access_token = session.get("github_token")
    if not access_token:
        return jsonify({"error": "Unauthorized"}), 401

    repos_url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(repos_url, headers=headers)

    current_app.logger.info(f"Github Repos: {response.json()}")

    return jsonify(response.json())
