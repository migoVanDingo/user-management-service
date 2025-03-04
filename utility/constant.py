import os


class Constant:
    service_port = 5014
    service = "user-management-service"

    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI = "http://localhost:5014/api/github/callback"
    SECRET_KEY = os.getenv("JWT_SECRET_KEY") 

    services = {
        "JOB": {
            "PORT": "5017",
            "ENDPOINT": {
                "CREATE-JOB": "/api/job/new",
            }
        },
        
    }


    base_url = "http://localhost:"
    dao_port = "5010"

    dao = {
        "create": "/api/create",
        "read": "/api/read",
        "list": "/api/read_list",
        "update": "/api/update",
        "delete": "/api/delete"
    }

    table = {
        "USER": "user",
        "USER_REGISTRATION": "user_registration",
        "USER_ROLES": "user_roles",
    }

    delimeter = {
        "USER": "__",

    }


    files = {
        "metadata": "-metadata.json"
    }


