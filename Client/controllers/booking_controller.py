from .api_controller import ApiController
from models import Booking
import json

class BookingController:
    def __init__(self, api: ApiController):
        self.api = api

    def create_booking(self, user_id, flight_id):
        data = {"frequentFlyerId": user_id, "flightId": flight_id}
        res = self.api.post("/bookings", json=data)

        # Check if the response indicates an error
        if isinstance(res, dict) and "message" in res:
            # Backend returned an error (like Shabbat)
            raise Exception(json.dumps(res))

        return Booking(**res)

    def list_user_bookings(self, user_id):
        res = self.api.get("/bookings", params={"userId": user_id})
        return [Booking(**b) for b in res]
