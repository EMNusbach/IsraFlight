from PySide6.QtCore import QObject, Signal
from .api_controller import ApiController


class FrequentFlyerController(QObject):
    # Define signals properly after inheriting QObject

    def __init__(self, api: ApiController):
        super().__init__()  # Initialize QObject
        self.api = api
    
    def register(self, data: dict):
        try:
            response = self.api.post("/frequentflyers", json=data)
            
            # Continue only if user creation succeeded
            authData = {
                "username": data["Username"],
                "password": data["Password"],
                "role": "frequentFlyer"
            }

            self.api.post("/auths", json=authData)

            return {"success": True, "data": response}

        except Exception as e:
            if hasattr(e, 'response') and e.response is not None:
                return {"success": False, "error": e.response.text}
            return {"success": False, "error": str(e)}


    def get_full_name(self, user_id: int):
        # ApiController.get already returns JSON, not Response
        try:
            data = self.api.get(f"FrequentFlyers/{user_id}")
            return data.get("fullName", "Passenger")
        except Exception as e:
            print(f"Error fetching frequent flyer {user_id}: {e}")
            return "Passenger"
