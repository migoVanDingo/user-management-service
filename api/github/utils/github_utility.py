import secrets
from flask import current_app, redirect, session
import requests
from utility.constant import Constant


class GithubUtility:
    @staticmethod
    def github_oauth(flow_type: str):
        """Redirects user to GitHub OAuth page."""
        state_token = secrets.token_urlsafe(16)  # Generate a random token
        session['github_oauth_state'] = state_token  # Store in session
        github_auth_url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={Constant.GITHUB_CLIENT_ID}&redirect_uri={Constant.GITHUB_REDIRECT_URI}&scope=repo,user"
            f"&state={state_token}-{flow_type}"
        )

        current_app.logger.info(f"Github auth url: {github_auth_url}")
        return redirect(github_auth_url)
    
    @staticmethod
    def verify_oauth_state(state: str):
        """Verify OAuth state token."""
        expected_state = session.pop('github_oauth_state', None)   
        received_state, flow_type = state.rsplit("-", 1)
        if not expected_state or expected_state != received_state:
            return False, ""
        
        return True, flow_type
    
    @staticmethod
    def fetch_github_email(access_token):
        """Fetch user's primary GitHub email address"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Get user's email addresses
        response = requests.get("https://api.github.com/user/emails", headers=headers)
        
        if response.status_code == 200:
            emails = response.json()
            # Find the primary email
            for email in emails:
                if email.get("primary") and email.get("verified"):
                    return email["email"]
        return None