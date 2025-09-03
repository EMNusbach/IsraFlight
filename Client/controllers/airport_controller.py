from controllers.api_controller import ApiController


class AirportController:
    def __init__(self, api: ApiController):
        self.api = api
        
    def get_all_airports(self):
        return self.api.get("airports")
        
    def get_airport_by_id(self, airport_id):
        return self.api.get(f"airports/{airport_id}")