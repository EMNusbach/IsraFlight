from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QDateEdit, QSpinBox, QComboBox, QMessageBox, QScrollArea,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import QDate, Qt
from datetime import datetime
from fpdf import FPDF

from controllers.airport_controller import AirportController
from controllers.api_controller import ApiController
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from models import Flight, Airport


class BookFlightWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_flight = None

        # Controllers
        api = ApiController(base_url="http://localhost:5126/api")
        self.booking_ctrl = BookingController(api)
        self.flight_ctrl = FlightController(api)
        self.airport_ctrl = AirportController(api)

        # Airports
        self.airports = [Airport(**a) for a in self.airport_ctrl.get_all_airports()]

        self.setWindowTitle("Book a Flight")
        self.setFixedSize(700, 750)
        self.setWindowFlags(Qt.Window)

        self.setup_styling()
        self.init_ui()

    def setup_styling(self):
        self.setStyleSheet("""
            QWidget#mainFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc, stop:1 #e2e8f0);
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 20px;
            }

            QWidget#header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b6cb0, stop:1 #2c5282);
                border-bottom: 2px solid #2a4365;
            }

            QLabel#titleLabel {
                font-size: 20pt;
                font-weight: bold;
                color: white;
            }

            QPushButton#closeButton {
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                color: white;
                font-size: 14pt;
                font-weight: bold;
                padding: 6px 12px;
            }

            QPushButton#closeButton:hover {
                background: rgba(255,255,255,0.2);
            }

            QLabel#label {
                font-size: 12pt;
                font-weight: 500;
                color: #2d3748;
            }

            QLineEdit, QSpinBox, QComboBox, QDateEdit {
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 6px;
                font-size: 12pt;
            }

            QPushButton#actionButton {
                font-size: 14pt;
                font-weight: 600;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 20px;
                min-height: 50px;
                text-align: center;
            }

            QPushButton#searchButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
            }

            QPushButton#searchButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #38a169, stop:1 #2f855a);
            }

            QPushButton#bookButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
            }

            QPushButton#bookButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3182ce, stop:1 #2b6cb0);
            }

            QFrame#flightCard {
                border: 1px solid #cbd5e0;
                border-radius: 12px;
                padding: 15px;
                background-color: white;
            }
        """)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Main Frame with shadow
        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 10)
        self.main_frame.setGraphicsEffect(shadow)
        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.setSpacing(25)
        frame_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = self.create_header()
        frame_layout.addWidget(header)

        # Form
        form_container = self.create_form_container()
        frame_layout.addWidget(form_container)

        # Buttons
        buttons_layout = self.create_buttons()
        frame_layout.addLayout(buttons_layout)

        # Flight results
        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_area.setWidget(self.results_container)
        self.results_area.hide()
        frame_layout.addWidget(self.results_area)

        main_layout.addWidget(self.main_frame)

    def create_header(self):
        header = QFrame()
        header.setObjectName("header")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        icon = QLabel("✈️")
        icon.setStyleSheet("font-size: 28pt; color: white;")
        layout.addWidget(icon)

        title = QLabel("Book Your Flight")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        return header

    def create_form_container(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        airport_names = [f"{a.city} ({a.code})" for a in self.airports]

        # From / To
        for label_text, combo_attr in [("From", "from_input"), ("To", "to_input")]:
            lbl = QLabel(label_text)
            lbl.setObjectName("label")
            layout.addWidget(lbl)
            combo = QComboBox()
            combo.addItems(airport_names)
            setattr(self, combo_attr, combo)
            layout.addWidget(combo)

        # Departure date
        lbl_date = QLabel("Departure Date")
        lbl_date.setObjectName("label")
        layout.addWidget(lbl_date)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Passengers
        lbl_pass = QLabel("Passengers")
        lbl_pass.setObjectName("label")
        layout.addWidget(lbl_pass)
        self.passengers_input = QSpinBox()
        self.passengers_input.setMinimum(1)
        self.passengers_input.setMaximum(9)
        layout.addWidget(self.passengers_input)

        # Travel Class
        lbl_class = QLabel("Travel Class")
        lbl_class.setObjectName("label")
        layout.addWidget(lbl_class)
        self.class_input = QComboBox()
        self.class_input.addItems(["Economy", "Premium Economy", "Business", "First Class"])
        layout.addWidget(self.class_input)

        return frame

    def create_buttons(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.close)

        self.submit_btn = QPushButton("Search Flights")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setObjectName("searchButton")
        self.submit_btn.clicked.connect(self.search_flights)

        layout.addWidget(cancel_btn)
        layout.addWidget(self.submit_btn)
        return layout

    # Rest of your methods like search_flights, create_flight_card, book_flight remain unchanged


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

        # If no exact matches, show all flights
        if not matched:
            matched = flights
            QMessageBox.information(self, "No Exact Matches", "No flights match your criteria. Showing all available flights.")

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
        try:
            # Attempt to create booking via backend
            booking = self.booking_ctrl.create_booking(self.user_id, flight.id)
            QMessageBox.information(
                self,
                "Booking Successful",
                f"Booking ID: {booking.id}\nFlight: {booking.flightId}"
            )
            self.generate_pdf_ticket(booking)
            self.close()

        except Exception as e:
            # Try to parse backend JSON error
            import json
            try:
                error_data = json.loads(str(e))
                message = error_data.get("message", "Booking failed")
                parasha = error_data.get("parasha")
                entry = error_data.get("shabbatEntry")
                exit = error_data.get("shabbatExit")
                if parasha and entry and exit:
                    message += f"\nParasha: {parasha}\nShabbat: {entry} → {exit}"
            except Exception:
                message = str(e)  # fallback if parsing fails

            QMessageBox.warning(self, "Booking Failed", message)



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
