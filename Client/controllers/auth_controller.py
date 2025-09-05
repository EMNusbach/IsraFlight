from PySide6.QtCore import QObject, Signal
from .api_controller import ApiController
from models import Auth

class AuthController(QObject):
    # Define signals properly after inheriting QObject
    login_success = Signal(object)  # emits User object
    login_failure = Signal(str)      # emits error message

    def __init__(self, api: ApiController):
        super().__init__()  # Initialize QObject
        self.api = api

    def login(self, username, password):
        try:
            data = {"Username": username, "Password": password}
            res = self.api.post("/Auths/login", json=data)

            auth = res.get("auth")
            if auth:
                user_obj = Auth(
                    Id=int(auth.get("id")),
                    Username=auth.get("username"),
                    Role=auth.get("role")
                )

                self.login_success.emit(user_obj)
                return

            self.login_failure.emit("Invalid response from server")

        except Exception as e:
            self.login_failure.emit(str(e))



   