class Cookie:
    def __init__(self):
        pass

    def set_cookie(self, response, key, value):
        response.set_cookie(key, value)
        return response