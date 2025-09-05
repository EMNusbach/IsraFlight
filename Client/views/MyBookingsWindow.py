from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from controllers.airport_controller import AirportController
from services.pdf_service import generate_ticket_pdf
from controllers.frequentFlyer_controller import FrequentFlyerController


class MyBookingsWindow(QWidget):
    def __init__(self, user_id, api):
        super().__init__()
        self.user_id = user_id
        self.booking_controller = BookingController(api)
        self.flight_controller = FlightController(api)
        self.airport_controller = AirportController(api)
        self.setWindowTitle("My Bookings - IsraFlight")
        self.setStyleSheet("background-color: #F4F6F8; font-family: Arial;")
        self.resize(1000, 600)
        self.init_ui()
        self.populate_bookings()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        header = QLabel("🧾 My Bookings")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)

        # Scroll area for bookings
        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_area.setWidget(self.results_container)
        main_layout.addWidget(self.results_area)

    def populate_bookings(self):
        user_bookings = self.booking_controller.list_user_bookings(self.user_id)
        print("user_id:", self.user_id)

        # Clear previous cards
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not user_bookings:
            empty_label = QLabel("No bookings found.")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 18px; color: #555; margin: 20px;")
            self.results_layout.addWidget(empty_label)
            return

        # Create a card for each booking
        for booking in user_bookings:
            try:
                flight = self.flight_controller.get_flight_by_id(booking.flightId)
            except Exception:
                print(f"Flight not found for booking {booking.id}")
                continue

            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet("""
                QFrame {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: white;
                    padding: 10px;
                    margin-bottom: 10px;
                }
            """)
            layout = QVBoxLayout(card)

            # Header
            header_layout = QHBoxLayout()
            header_layout.addWidget(QLabel(f"✈️ Flight {flight.id}"))
            header_layout.addStretch()
            header_layout.addWidget(QLabel(f"Booking ID: {booking.id}"))
            layout.addLayout(header_layout)

            # Route
            route_text = f"From: {self.get_airport_name(flight.departureAirportId)} → To: {self.get_airport_name(flight.arrivalAirportId)}"
            route = QLabel(route_text)
            route.setStyleSheet("font-weight: bold; font-size: 16px;")
            layout.addWidget(route)

            # Times
            times = QLabel(f"Departure: {flight.departureTime}   Arrival: {flight.arrivalTime}")
            layout.addWidget(times)

            # Price
            price = QLabel(f"Price: ${getattr(flight, 'price', 'N/A')}")
            layout.addWidget(price)

            # PDF button
            pdf_btn = QPushButton("📄 Download Ticket PDF")
            pdf_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
            """)
            pdf_btn.clicked.connect(lambda _, b=booking: self.generate_pdf(b))
            layout.addWidget(pdf_btn, alignment=Qt.AlignRight)

            self.results_layout.addWidget(card)

    def get_airport_name(self, airport_id):
        airports = self.airport_controller.get_all_airports()
        for a in airports:
            if a.get("id") == airport_id:
                return a.get("name")
        return "Unknown Airport"

    def generate_pdf(self, booking):
        try:
            flight = self.flight_controller.get_flight_by_id(booking.flightId)
        except Exception:
            QMessageBox.warning(self, "Error", "Flight not found")
            return

        # Get traveler name automatically
        frequent_flyer_controller = FrequentFlyerController(self.booking_controller.api)
        traveler_name = frequent_flyer_controller.get_full_name(self.user_id)

        # Get airport names automatically
        dep_airport_name = self.get_airport_name(flight.departureAirportId)
        arr_airport_name = self.get_airport_name(flight.arrivalAirportId)

        # Generate PDF
        pdf_path = generate_ticket_pdf(
            booking,
            flight,
            traveler_name=traveler_name,
            dep_airport_name=dep_airport_name,
            arr_airport_name=arr_airport_name
        )

        # Open PDF automatically
        import webbrowser
        webbrowser.open_new(pdf_path)



