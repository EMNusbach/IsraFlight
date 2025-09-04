from PySide6.QtCore import QObject, Signal
from .api_controller import ApiController


class FrequentFlyerController(QObject):
    # Define signals properly after inheriting QObject

    def __init__(self, api: ApiController):
        super().__init__()  # Initialize QObject
        self.api = api
    
    def register(self, data: dict):
        response = self.api.post("/frequentflyers", json=data)
        authData = {
            "username": data["Username"],
            "password": data["Password"],
            "role": "frequentFlyer"
        }

        self.api.post("/auths", json=authData )
        return response
