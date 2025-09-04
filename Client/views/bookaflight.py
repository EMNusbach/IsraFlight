from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QDateEdit, QSpinBox, QComboBox, QMessageBox, QScrollArea
)
from PySide6.QtCore import QDate, Qt
from datetime import datetime
from fpdf import FPDF
from controllers.airport_controller import AirportController
from controllers.api_controller import ApiController
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from models import Flight, Airport  # Make sure your dataclasses exist


class BookFlightWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_flight = None

        # Initialize controllers
        api = ApiController(base_url="http://localhost:5126/api")
        self.booking_ctrl = BookingController(api)
        self.flight_ctrl = FlightController(api)
        self.airport_ctrl = AirportController(api)

        # Fetch airports
        self.airports = [Airport(**a) for a in self.airport_ctrl.get_all_airports()]

        self.setWindowTitle("Book a Flight")
        self.setFixedSize(600, 700)
        self.setWindowFlags(Qt.Window)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Header
        main_layout.addWidget(self.create_header())

        # Form
        main_layout.addWidget(self.create_form_container())

        # Buttons
        main_layout.addLayout(self.create_buttons())

        # Flight results area
        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_container.setLayout(self.results_layout)
        self.results_area.setWidget(self.results_container)
        self.results_area.hide()
        main_layout.addWidget(self.results_area)

    # Header with title and close button
    def create_header(self):
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.addWidget(QLabel("✈️"))
        title = QLabel("Book Your Flight")
        title.setStyleSheet("font-weight:bold; font-size:20px;")
        layout.addWidget(title)
        layout.addStretch()
        close_btn = QPushButton("✕")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        return header

    # Form for selecting airports, date, passengers, class
    def create_form_container(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        airport_names = [f"{a.city} ({a.code})" for a in self.airports]

        # From airport
        layout.addWidget(QLabel("From"))
        self.from_input = QComboBox()
        self.from_input.addItems(airport_names)
        layout.addWidget(self.from_input)

        # To airport
        layout.addWidget(QLabel("To"))
        self.to_input = QComboBox()
        self.to_input.addItems(airport_names)
        layout.addWidget(self.to_input)

        # Departure date
        layout.addWidget(QLabel("Departure Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Passengers
        layout.addWidget(QLabel("Passengers"))
        self.passengers_input = QSpinBox()
        self.passengers_input.setMinimum(1)
        self.passengers_input.setMaximum(9)
        layout.addWidget(self.passengers_input)

        # Class
        layout.addWidget(QLabel("Travel Class"))
        self.class_input = QComboBox()
        self.class_input.addItems(["Economy", "Premium Economy", "Business", "First Class"])
        layout.addWidget(self.class_input)

        return frame

    # Cancel/Search buttons
    def create_buttons(self):
        layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        self.submit_btn = QPushButton("Search Flights")
        self.submit_btn.clicked.connect(self.search_flights)
        layout.addWidget(cancel_btn)
        layout.addWidget(self.submit_btn)
        return layout

    # Search flights based on form input
    def search_flights(self):
        from_id = self.get_airport_id(self.from_input)
        to_id = self.get_airport_id(self.to_input)
        departure_date = self.date_input.date().toPython()

        if from_id == -1 or to_id == -1 or from_id == to_id:
            QMessageBox.warning(self, "Validation Error", "Select valid departure and destination airports")
            return

        flights = self.flight_ctrl.get_all_flights()
        matched = [
            f for f in flights
            if f.departureAirportId == from_id
            and f.arrivalAirportId == to_id
            and datetime.fromisoformat(f.departureTime).date() == departure_date
        ]

        if not matched:
            QMessageBox.information(self, "No Flights", "No flights found")
            self.results_area.hide()
            return

        # Clear old results
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add new flight cards
        for f in matched:
            flight_card = self.create_flight_card(f)
            self.results_layout.addWidget(flight_card)

        self.results_area.show()

    # Create a card widget for each flight
    def create_flight_card(self, flight: Flight):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(card)

        # Header: Flight number and price
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(f"✈️ Flight {flight.id}"))
        header_layout.addStretch()
        price_lbl = QLabel(f"${flight.price:,.2f}")
        price_lbl.setStyleSheet("font-weight: bold; font-size: 16px;")
        header_layout.addWidget(price_lbl)
        layout.addLayout(header_layout)

        # Times
        times = QLabel(f"{datetime.fromisoformat(flight.departureTime).strftime('%H:%M')} "
                       f"→ {datetime.fromisoformat(flight.arrivalTime).strftime('%H:%M')}")
        layout.addWidget(times)

        # Route
        route = QLabel(f"From: {self.get_airport_name(flight.departureAirportId)}   "
                       f"To: {self.get_airport_name(flight.arrivalAirportId)}")
        layout.addWidget(route)

        # Book button
        book_btn = QPushButton("Book")
        book_btn.clicked.connect(lambda: self.book_flight(flight))
        layout.addWidget(book_btn, alignment=Qt.AlignRight)

        card.setStyleSheet("""
            QFrame { border: 1px solid #ccc; border-radius: 10px; padding: 10px; background-color: white; }
            QPushButton { background-color: #0078D7; color: white; border-radius: 5px; padding: 6px 12px; }
            QPushButton:hover { background-color: #005A9E; }
        """)
        return card

    # Get airport name from ID
    def get_airport_name(self, airport_id):
        for a in self.airports:
            if a.id == airport_id:
                return f"{a.city} ({a.code})"
        return str(airport_id)

    def get_airport_id(self, combo: QComboBox):
        index = combo.currentIndex()
        if 0 <= index < len(self.airports):
            return self.airports[index].id
        return -1

    # Check Shabbat restriction and book flight
    def book_flight(self, flight: Flight):
        arrival_time = datetime.fromisoformat(flight.arrivalTime)
        if (arrival_time.weekday() == 4 and arrival_time.hour >= 18) or arrival_time.weekday() == 5:
            QMessageBox.warning(self, "Shabbat Restriction", "Flight lands on Shabbat.")
            return

        try:
            booking = self.booking_ctrl.create_booking(self.user_id, flight.id)
            QMessageBox.information(self, "Booking Successful",
                        f"Booking ID: {booking.id}\nFlight: {booking.flightId}")
            self.generate_pdf_ticket(booking)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Booking Failed", str(e))

    # Generate PDF ticket
    def generate_pdf_ticket(self, booking):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, f"Booking ID: {booking.id}", ln=True)
        pdf.cell(0, 10, f"Flight ID: {booking.flightId}", ln=True)
        pdf.cell(0, 10, f"From: {self.from_input.currentText()}", ln=True)
        pdf.cell(0, 10, f"To: {self.to_input.currentText()}", ln=True)
        pdf.cell(0, 10, f"Date: {self.date_input.date().toString('yyyy-MM-dd')}", ln=True)
        pdf.cell(0, 10, f"Passengers: {self.passengers_input.value()}", ln=True)
        pdf.cell(0, 10, f"Class: {self.class_input.currentText()}", ln=True)
        pdf.output("ticket.pdf")
