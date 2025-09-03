
from .api_controller import ApiController
from models import Booking

class BookingController:
    def __init__(self, api: ApiController):
        self.api = api

    def create_booking(self, user_id, flight_id, seat=None):
        data = {"userId": user_id, "flightId": flight_id, "seat": seat}
        res = self.api.post("/bookings", json=data)
        return Booking(**res)

    def list_user_bookings(self, user_id):
        res = self.api.get(f"/bookings", params={"userId": user_id})
        return [Booking(**b) for b in res]
