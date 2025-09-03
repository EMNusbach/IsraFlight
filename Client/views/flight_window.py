from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QDateTimeEdit, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont
from models import Flight

from controllers.plane_controller import PlaneController
from controllers.airport_controller import AirportController

class FlightWindow(QMainWindow):
    def __init__(self, flight_controller, plane_controller, airport_controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Flight Management")
        self.setMinimumSize(1200, 800)
        self.flight_controller = flight_controller
        self.plane_controller = plane_controller
        self.airport_controller = airport_controller

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self.init_ui()
        self.load_flights()

    def init_ui(self):
        title = QLabel("✈️ Manage Flights")
        title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #2d3748;")
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)

        self.flights_area = QScrollArea()
        self.flights_area.setWidgetResizable(True)
        self.flights_container = QWidget()
        self.flights_layout = QVBoxLayout(self.flights_container)
        self.flights_area.setWidget(self.flights_container)

        self.main_layout.addWidget(self.flights_area)

        # Add Flight Button
        add_button = QPushButton("➕ Add New Flight")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #38a169;
                color: white;
                padding: 12px 24px;
                font-size: 14pt;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2f855a;
            }
        """)
        add_button.clicked.connect(self.open_add_flight_form)
        self.main_layout.addWidget(add_button)

    def load_flights(self):
        for i in reversed(range(self.flights_layout.count())):
            item = self.flights_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        flights = self.flight_controller.get_all_flights()
        for flight in flights:
            self.flights_layout.addWidget(self.create_flight_card(flight))

    def create_flight_card(self, flight: Flight):

        # Fetch related data
        plane = self.plane_controller.get_plane_by_id(flight.planeId)
        dep_airport = self.airport_controller.get_airport_by_id(flight.departureAirportId)
        arr_airport = self.airport_controller.get_airport_by_id(flight.arrivalAirportId)

        dep_name = dep_airport.get('code', 'Unknown')
        arr_name = arr_airport.get('code', 'Unknown')
        nickname = plane.get('nickname', 'Unknown')

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #cbd5e0;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        layout = QHBoxLayout(card)
        print(flight)
        info = QLabel(f"""
            <b>Flight ID:</b> {flight.id} <br>
            <b>Plane:</b> {nickname} <br>
            <b>From:</b> {dep_name} | <b>To:</b> {arr_name}<br>
            <b>Departure:</b> {flight.departureTime}<br>
            <b>Arrival:</b> {flight.arrivalTime}<br>
            <b>Price:</b> ${flight.price}
        """)
        layout.addWidget(info)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e53e3e;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c53030;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_flight(flight.id))
        layout.addWidget(delete_btn)

        return card

    def delete_flight(self, flight_id):
        self.flight_controller.delete_flight(flight_id)
        self.load_flights()

    def open_add_flight_form(self):
        self.add_form = QFrame()
        self.add_form.setStyleSheet("""
            QFrame {
                background: #edf2f7;
                border: 1px solid #cbd5e0;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(self.add_form)

        # Plane 
        self.plane_input = QComboBox()
        planes = self.plane_controller.get_all_planes()

        self.plane_map = {}  # nickname → id
        for plane in planes:
            nickname = plane.get('nickname', f"Plane {plane['id']}")
            self.plane_input.addItem(nickname, plane['id'])
            self.plane_map[nickname] = plane['id']

        layout.addWidget(QLabel("Plane:"))
        layout.addWidget(self.plane_input)

        # === Airports (Departure & Arrival) ===
        self.departure_airport = QComboBox()
        self.arrival_airport = QComboBox()
        airports = self.airport_controller.get_all_airports()

        self.airport_map = {}  # name → id
        for airport in airports:
            name = airport.get('name', f"Airport {airport['id']}")
            self.departure_airport.addItem(name, airport['id'])
            self.arrival_airport.addItem(name, airport['id'])
            self.airport_map[name] = airport['id']

        layout.addWidget(QLabel("Departure Airport:"))
        layout.addWidget(self.departure_airport)

        layout.addWidget(QLabel("Arrival Airport:"))
        layout.addWidget(self.arrival_airport)

        # Departure time
        self.departure_time = QDateTimeEdit()
        self.departure_time.setCalendarPopup(True)
        self.departure_time.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel("Departure Time:"))
        layout.addWidget(self.departure_time)

        # Arrival time
        self.arrival_time = QDateTimeEdit()
        self.arrival_time.setCalendarPopup(True)
        self.arrival_time.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel("Arrival Time:"))
        layout.addWidget(self.arrival_time)

        # Price
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("$")
        self.price_input.setRange(0, 10000)
        self.price_input.setDecimals(2)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_input)

        # Submit
        submit_btn = QPushButton("Submit Flight")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3182ce;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2b6cb0;
            }
        """)
        submit_btn.clicked.connect(self.submit_flight)
        layout.addWidget(submit_btn)

        self.main_layout.addWidget(self.add_form)

    def submit_flight(self):
        data = {
            "PlaneId": self.plane_input.currentData(),
            "DepartureAirportId": self.departure_airport.currentData(),
            "ArrivalAirportId": self.arrival_airport.currentData(),
            "DepartureTime": self.departure_time.dateTime().toString(Qt.ISODate),
            "ArrivalTime": self.arrival_time.dateTime().toString(Qt.ISODate),
            "Price": float(self.price_input.value()),
        }
        self.flight_controller.create_flight(data)
        self.add_form.deleteLater()
        self.load_flights()
