# controllers/admin_controller.py
from PySide6.QtCore import QObject, Signal
from .api_controller import ApiController
from .plane_controller import PlaneController
from .flight_controller import FlightController


class AdminController(QObject):
    # Signals for plane creation
    plane_created = Signal(object)
    plane_submit_success = Signal(str)
    plane_submit_failure = Signal(str)

    # Signals for flight scheduling
    flight_submit_success = Signal(str)
    flight_submit_failure = Signal(str)

    def __init__(self, api=None):
        super().__init__()
        self.api = api or ApiController()
        self.plane_controller = PlaneController(self.api)
        self.flight_controller = FlightController(self.api)

    def submit_plane(self, data):
        try:
            plane = self.plane_controller.create_plane(
                manufacturer=data["manufacturer"],
                nickname=data["nickname"],
                year=data["year"],
                image_url=data.get("image_url")  # pass image URL now
            )
            self.plane_created.emit(plane)
            self.plane_submit_success.emit("Plane added successfully.")
        except Exception as e:
            self.plane_submit_failure.emit(str(e))
            


    def submit_flight(self, data):
        try:
            self.flight_controller.create_flight(
                plane_id=data["plane_id"],
                origin=data["origin"],
                destination=data["destination"],
                departure=data["departure"],
                arrival_estimate=data["arrival_estimate"],
            )
            self.flight_submit_success.emit("Flight scheduled successfully.")
        except Exception as e:
            self.flight_submit_failure.emit(str(e))
