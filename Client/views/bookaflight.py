from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QDateEdit, QSpinBox, QComboBox, QListWidget, QListWidgetItem,
    QMessageBox
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QCursor
from datetime import datetime
from fpdf import FPDF  # pip install fpdf2
from controllers.airport_controller import AirportController

from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from models import Flight  # Make sure Flight dataclass exists
from models import Airport


class BookFlightWindow(QWidget):
    def __init__(self, user_id, api):
        super().__init__()
        self.user_id = user_id
        self.api = api
        self.booking_ctrl = BookingController(api)
        self.flight_ctrl = FlightController(api)
        self.airport_ctrl = AirportController(api)  # <-- add this

        self.selected_flight = None

        self.airports = [Airport(**a) for a in self.airport_ctrl.get_all_airports()]


        self.setWindowTitle("Book a Flight")
        self.setFixedSize(600, 700)
        self.setWindowFlags(Qt.Window)  # Normal window

        self.setup_styling()
        self.init_ui()

    def setup_styling(self):
        self.setStyleSheet("""
            /* Add your custom styling here */
        """)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.main_frame = QFrame()
        main_layout.addWidget(self.main_frame)

        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)

        frame_layout.addWidget(self.create_header())
        frame_layout.addWidget(self.create_form_container())
        frame_layout.addLayout(self.create_buttons())

        # Flight list widget
        self.flight_list_widget = QListWidget()
        self.flight_list_widget.itemClicked.connect(self.on_flight_selected)
        frame_layout.addWidget(self.flight_list_widget)
        self.flight_list_widget.hide()

    def create_header(self):
        header = QFrame()
        layout = QHBoxLayout(header)

        layout.addWidget(QLabel("✈️"))
        title = QLabel("Book Your Flight")
        title.setStyleSheet("font-weight:bold; font-size:20px;")
        layout.addWidget(title)
        layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.clicked.connect(self.close)  # Close window
        layout.addWidget(close_btn)

        return header

    def create_form_container(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Fetch airports
        airport_names = [f"{a.city} ({a.code})" for a in self.airports]

        # From
        self.from_input = QComboBox()
        self.from_input.addItems(airport_names)
        layout.addWidget(QLabel("From"))
        layout.addWidget(self.from_input)

        # To
        self.to_input = QComboBox()
        self.to_input.addItems(airport_names)
        layout.addWidget(QLabel("To"))
        layout.addWidget(self.to_input)

        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Departure Date"))
        layout.addWidget(self.date_input)

        # Passengers
        self.passengers_input = QSpinBox()
        self.passengers_input.setMinimum(1)
        self.passengers_input.setMaximum(9)
        self.passengers_input.setValue(1)
        layout.addWidget(QLabel("Passengers"))
        layout.addWidget(self.passengers_input)

        # Class
        self.class_input = QComboBox()
        self.class_input.addItems(["Economy", "Premium Economy", "Business", "First Class"])
        layout.addWidget(QLabel("Travel Class"))
        layout.addWidget(self.class_input)

        return frame


    def create_buttons(self):
        layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        self.submit_btn = QPushButton("Search Flights")
        self.submit_btn.clicked.connect(self.search_flights)

        layout.addWidget(cancel_btn)
        layout.addWidget(self.submit_btn)
        return layout

    def get_airport_id(self, combo: QComboBox):
        index = combo.currentIndex()
        if 0 <= index < len(self.airports):
            return self.airports[index].id
        return -1




    def is_shabbat(self, arrival_time_str):
        arrival = datetime.fromisoformat(arrival_time_str)
        return (arrival.weekday() == 4 and arrival.hour >= 18) or arrival.weekday() == 5

    def search_flights(self):
        # Get selected airport IDs
        from_id = self.get_airport_id(self.from_input)
        to_id = self.get_airport_id(self.to_input)
        departure_date = self.date_input.date().toPython()
        passengers = self.passengers_input.value()

        if from_id == -1 or to_id == -1 or from_id == to_id:
            QMessageBox.warning(self, "Validation Error",
                                "Select valid departure and destination airports")
            return

        try:
            flights = self.flight_ctrl.get_all_flights()

            # Match flights based on departure/arrival airports and date
            matched = [
                f for f in flights
                if f.departureAirportId == from_id
                and f.arrivalAirportId == to_id
                and datetime.fromisoformat(f.departureTime).date() == departure_date
            ]

            if not matched:
                QMessageBox.information(self, "No Flights", "No flights found")
                self.flight_list_widget.hide()
                return

            # Populate flight list widget
            self.flight_list_widget.clear()
            for f in matched:
                item = QListWidgetItem(
                    f"Flight {f.id} | {datetime.fromisoformat(f.departureTime).strftime('%H:%M')} | ${f.price}"
                )
                item.setData(Qt.UserRole, f)
                self.flight_list_widget.addItem(item)

            self.flight_list_widget.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def on_flight_selected(self, item: QListWidgetItem):
        self.selected_flight = item.data(Qt.UserRole)

        # Check for Shabbat restriction
        arrival_time = datetime.fromisoformat(self.selected_flight.arrivalTime)
        if (arrival_time.weekday() == 4 and arrival_time.hour >= 18) or arrival_time.weekday() == 5:
            QMessageBox.warning(self, "Shabbat Restriction",
                                "Flight lands on Shabbat.")
            return

        try:
            booking = self.booking_ctrl.create_booking(self.user_id, self.selected_flight.id)
            QMessageBox.information(self, "Booking Successful",
                                    f"Booking ID: {booking.id}\nFlight: {self.selected_flight.id}")
            self.generate_pdf_ticket(booking)
            self.close()  # Close window after booking
        except Exception as e:
            QMessageBox.critical(self, "Booking Failed", str(e))
            

    def generate_pdf_ticket(self, booking):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, f"Booking ID: {booking.id}", ln=True)
        pdf.cell(0, 10, f"Flight ID: {booking.flightId}", ln=True)
        pdf.cell(0, 10, f"From: {self.from_input.text()}", ln=True)
        pdf.cell(0, 10, f"To: {self.to_input.text()}", ln=True)
        pdf.cell(0, 10, f"Date: {self.date_input.date().toString('yyyy-MM-dd')}", ln=True)
        pdf.cell(0, 10, f"Passengers: {self.passengers_input.value()}", ln=True)
        pdf.cell(0, 10, f"Class: {self.class_input.currentText()}", ln=True)
        pdf.output("ticket.pdf")
