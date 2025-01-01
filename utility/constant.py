class Constant:
    service_port = 5014
    service = "user-management-service"


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
    }

    delimeter = {
        "USER": "__",

    }


    files = {
        "metadata": "-metadata.json"
    }


