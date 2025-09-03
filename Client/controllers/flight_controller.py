from .api_controller import ApiController
from models import Flight

class FlightController:
    def __init__(self, api: ApiController):
        self.api = api

    def get_all_flights(self):
        data = self.api.get("flights")
        return [Flight(**item) for item in data]

    def create_flight(self, flight_data):
        return self.api.post("flights", json=flight_data)

    def delete_flight(self, flight_id):
        return self.api.delete(f"flights/{flight_id}")
    
    def update_flight(self, plane_id, data):
        return self.api.put(f"flights/{plane_id}", data)  
