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

    def get_full_name(self, user_id: int):
        # ApiController.get already returns JSON, not Response
        try:
            data = self.api.get(f"FrequentFlyers/{user_id}")
            return data.get("fullName", "Passenger")
        except Exception as e:
            print(f"Error fetching frequent flyer {user_id}: {e}")
            return "Passenger"