import datetime


class PayloadUserSession:
    @staticmethod
    def form_user_session(user_id: str, refresh_token: str, ip: str = None):
        payload =  {
            "user_id": user_id,
            "refresh_token": refresh_token,
            "expires_at": f"{datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)}"
        }

        if ip:
            device_info = {
                "ip": ip
            }
            payload["device_info"] = device_info

        return payload
        