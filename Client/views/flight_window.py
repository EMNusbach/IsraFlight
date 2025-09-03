from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QDateTimeEdit, QComboBox, QDoubleSpinBox, QMessageBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QCursor, QFont
from models import Flight


class FlightWindow(QMainWindow):
    def __init__(self, flight_controller, plane_controller, airport_controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Flight Management - IsraFlight")
        self.setMinimumSize(1200, 800)
        self.flight_controller = flight_controller
        self.plane_controller = plane_controller
        self.airport_controller = airport_controller
        self.current_form = None  # Track current form (add/update)

        # === Central Layout ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Navigation Bar ===
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(80)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 20, 30, 20)

        # Back Button
        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.clicked.connect(self.close)

        # Title
        lbl_title = QLabel("✈ Manage Flights")
        lbl_title.setObjectName("titleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)

        # Brand
        lbl_brand = QLabel("IsraFlight")
        lbl_brand.setObjectName("brandLabel")
        lbl_brand.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch(1)
        nav_layout.addWidget(lbl_title)
        nav_layout.addStretch(1)
        nav_layout.addWidget(lbl_brand)
        main_layout.addWidget(nav_bar)

        # === Content Area ===
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)
        main_layout.addWidget(content_widget)

        # === Header Section ===
        header_section = QWidget()
        header_layout = QHBoxLayout(header_section)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Title and subtitle
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        main_title = QLabel("Flight Schedule")
        main_title.setObjectName("mainTitle")
        subtitle = QLabel("Manage your flight operations")
        subtitle.setObjectName("subtitle")

        title_layout.addWidget(main_title)
        title_layout.addWidget(subtitle)
        header_layout.addWidget(title_container)
        header_layout.addStretch()

        # Add Flight Button
        self.add_button = QPushButton("+ Add New Flight")
        self.add_button.setObjectName("addFlightButton")
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.clicked.connect(self.toggle_add_flight_form)
        header_layout.addWidget(self.add_button)

        self.main_layout.addWidget(header_section)

        # === Flights Scroll Area ===
        self.flights_area = QScrollArea()
        self.flights_area.setWidgetResizable(True)
        self.flights_area.setObjectName("flightsScrollArea")
        self.flights_container = QWidget()
        self.flights_layout = QVBoxLayout(self.flights_container)
        self.flights_layout.setSpacing(12)
        self.flights_layout.setContentsMargins(0, 0, 0, 0)
        self.flights_area.setWidget(self.flights_container)
        self.main_layout.addWidget(self.flights_area)

        # Load flights
        self.load_flights()

        # Apply styling
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f8fafc;
            }
            
            QWidget#contentWidget {
                background-color: #f8fafc;
            }
            
            QWidget#navBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                border-bottom: 2px solid #4a5568;
            }
            
            QPushButton#backButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 16pt;
                font-weight: bold;
                padding: 8px 12px;
                min-width: 35px;
                min-height: 25px;
            }
            
            QPushButton#backButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            QLabel#titleLabel {
                font-size: 20pt;
                font-weight: bold;
                color: white;
            }
            
            QLabel#brandLabel {
                font-weight: bold;
                color: white;
                font-size: 16pt;
                letter-spacing: 1px;
                min-width: 120px;
            }
            
            QLabel#mainTitle {
                font-size: 24pt;
                font-weight: bold;
                color: #1a202c;
            }
            
            QLabel#subtitle {
                font-size: 14pt;
                color: #718096;
            }
            
            QPushButton#addFlightButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                color: white;
                padding: 12px 24px;
                font-size: 14pt;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            
            QPushButton#addFlightButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
            
            QScrollArea#flightsScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollArea#flightsScrollArea QScrollBar:vertical {
                border: none;
                background-color: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
            
            /* Form Styling */
            QFrame#flightForm {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 0px;
            }
            
            QLabel#formTitle {
                font-size: 18pt;
                font-weight: bold;
                color: #1a202c;
                padding: 20px 20px 10px 15px;
            }
            
            QLabel.fieldLabel {
                font-size: 12pt;
                font-weight: 600;
                color: #4a5568;
                margin-bottom: 3px;
            }
            
            QComboBox, QDateTimeEdit, QDoubleSpinBox {
                padding: 10px 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 12pt;
                background: white;
                min-height: 20px;
                with: 300px
            }
            
            QComboBox:focus, QDateTimeEdit:focus, QDoubleSpinBox:focus {
                border-color: #1a202c;
                outline: none;
            }
            
            QPushButton.formButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                color: white;
                padding: 12px 20px;
                font-size: 13pt;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                min-width: 100px;
            }
            
            QPushButton.formButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
            
            QPushButton.cancelButton {
                background: #f7fafc;
                color: #4a5568;
                padding: 12px 20px;
                font-size: 13pt;
                font-weight: bold;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                min-width: 100px;
            }
            
            QPushButton.cancelButton:hover {
                background: #edf2f7;
                border-color: #cbd5e1;
            }
        """

    def load_flights(self):
        """Load and display all flights"""
        # Clear existing flights
        for i in reversed(range(self.flights_layout.count())):
            item = self.flights_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Load flights from controller
        flights = self.flight_controller.get_all_flights()
        
        if not flights:
            # Show empty state
            empty_label = QLabel("No flights scheduled yet")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                font-size: 16pt;
                color: #a0aec0;
                padding: 40px;
            """)
            self.flights_layout.addWidget(empty_label)
            return
        
        # Create flight cards
        for flight in flights:
            card = self.create_flight_card(flight)
            self.flights_layout.addWidget(card)

    def create_flight_card(self, flight: Flight):
        """Create a modern flight card similar to booking websites"""
        # Fetch related data
        plane_data = self.plane_controller.get_plane_by_id(flight.planeId) or {}
        dep_airport = self.airport_controller.get_airport_by_id(flight.departureAirportId) or {}
        arr_airport = self.airport_controller.get_airport_by_id(flight.arrivalAirportId) or {}

        # Extract display names
        plane_name = plane_data.get('Nickname', plane_data.get('nickname', f"Plane {flight.planeId}"))
        dep_code = dep_airport.get('Code', dep_airport.get('code', 'UNK'))
        arr_code = arr_airport.get('Code', arr_airport.get('code', 'UNK'))
        dep_city = dep_airport.get('City', dep_airport.get('city', 'Unknown'))
        arr_city = arr_airport.get('City', arr_airport.get('city', 'Unknown'))

        # Parse datetime strings
        try:
            dep_time = QDateTime.fromString(flight.departureTime, Qt.ISODate)
            arr_time = QDateTime.fromString(flight.arrivalTime, Qt.ISODate)
            dep_display = dep_time.toString("MMM dd, hh:mm")
            arr_display = arr_time.toString("MMM dd, hh:mm")
        except:
            dep_display = str(flight.departureTime)[:16]
            arr_display = str(flight.arrivalTime)[:16]

        # Create card
        card = QFrame()
        card.setObjectName("flightCard")
        card.setStyleSheet("""
            QFrame#flightCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 0px;
            }
            QFrame#flightCard:hover {
                border-color: #cbd5e1;
                background: #fefefe;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top section with flight info
        top_section = QWidget()
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(24, 20, 24, 16)
        top_layout.setSpacing(20)

        # Left side - Flight details
        left_side = QWidget()
        left_layout = QVBoxLayout(left_side)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # Flight ID and Plane
        flight_info = QLabel(f"IsraFlight • Flight ID: {flight.id}")
        flight_info.setStyleSheet("""
            font-size: 11pt;
            color: #1a202c;
            font-weight: bold;
        """)
        left_layout.addWidget(flight_info)

        top_layout.addWidget(left_side)

        # Center - Route information
        center_section = QWidget()
        center_layout = QVBoxLayout(center_section)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(12)

        # Route display
        route_layout = QHBoxLayout()
        route_layout.setSpacing(15)

        # Departure
        dep_widget = QWidget()
        dep_layout = QVBoxLayout(dep_widget)
        dep_layout.setContentsMargins(0, 0, 0, 0)
        dep_layout.setSpacing(2)

        dep_code_label = QLabel(dep_code)
        dep_code_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #1a202c;
        """)
        dep_city_label = QLabel(dep_city)
        dep_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        dep_time_label = QLabel(dep_display)
        dep_time_label.setStyleSheet("""
            font-size: 11pt;
            color: #1a202c;
            font-weight: 600;
        """)

        dep_layout.addWidget(dep_code_label)
        dep_layout.addWidget(dep_city_label)
        dep_layout.addWidget(dep_time_label)

        # Plane icon/arrow
        plane_label = QLabel("✈")
        plane_label.setAlignment(Qt.AlignCenter)
        plane_label.setStyleSheet("""
            font-size: 16pt;
            color: #64748b;
            margin: 10px;
        """)

        # Arrival
        arr_widget = QWidget()
        arr_layout = QVBoxLayout(arr_widget)
        arr_layout.setContentsMargins(0, 0, 0, 0)
        arr_layout.setSpacing(2)

        arr_code_label = QLabel(arr_code)
        arr_code_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #1a202c;
        """)
        arr_city_label = QLabel(arr_city)
        arr_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        arr_time_label = QLabel(arr_display)
        arr_time_label.setStyleSheet("""
            font-size: 11pt;
            color: #1a202c;
            font-weight: 600;
        """)

        arr_layout.addWidget(arr_code_label)
        arr_layout.addWidget(arr_city_label)
        arr_layout.addWidget(arr_time_label)

        route_layout.addWidget(dep_widget)
        route_layout.addWidget(plane_label)
        route_layout.addWidget(arr_widget)
        center_layout.addLayout(route_layout)

        # Plane name
        plane_label_widget = QLabel(f"Aircraft: {plane_name}")
        plane_label_widget.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        center_layout.addWidget(plane_label_widget)

        top_layout.addWidget(center_section)

        # Right side - Price and actions
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignTop)

        # Price
        price_label = QLabel(f"${flight.price:.2f}")
        price_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #1a202c;
        """)
        price_label.setAlignment(Qt.AlignRight)
        right_layout.addWidget(price_label)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        update_btn = QPushButton("Edit")
        update_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                color: white;
                padding: 8px 16px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
                min-width: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
        """)
        update_btn.setCursor(QCursor(Qt.PointingHandCursor))
        update_btn.clicked.connect(lambda: self.open_update_form(flight))

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #dc3545;
                color: white;
                padding: 8px 16px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 6px;
                border: none;
                min-width: 50px;
            }
            QPushButton:hover {
                background: #c82333;
            }
        """)
        delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        delete_btn.clicked.connect(lambda: self.delete_flight(flight.id))

        button_layout.addWidget(update_btn)
        button_layout.addWidget(delete_btn)
        right_layout.addLayout(button_layout)

        top_layout.addWidget(right_side)
        main_layout.addWidget(top_section)

        return card

    def toggle_add_flight_form(self):
        """Toggle the add flight form"""
        if self.current_form:
            self.current_form.deleteLater()
            self.current_form = None
            self.add_button.setText("+ Add New Flight")
        else:
            self.open_add_flight_form()

    def open_add_flight_form(self):
        """Open the add flight form"""
        self.current_form = self.create_flight_form("Add New Flight")
        self.main_layout.insertWidget(2, self.current_form)
        self.add_button.setText("Cancel")

    def open_update_form(self, flight: Flight):
        """Open the update flight form"""
        if self.current_form:
            self.current_form.deleteLater()
            
        self.current_form = self.create_flight_form("Update Flight", flight)
        self.main_layout.insertWidget(2, self.current_form)
        self.add_button.setText("Cancel")

    def create_flight_form(self, title, flight=None):
        """Create a form for adding or updating flights"""
        form = QFrame()
        form.setObjectName("flightForm")
        
        main_layout = QVBoxLayout(form)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("formTitle")
        main_layout.addWidget(title_label)

        # Form content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 10, 20, 20)
        content_layout.setSpacing(15)

        # Create form grid
        form_layout = QHBoxLayout()
        form_layout.setSpacing(30)

        # Left column
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(15)

        # Plane selection
        plane_label = QLabel("Aircraft")
        plane_label.setProperty("class", "fieldLabel")
        self.plane_input = QComboBox()
        planes = self.plane_controller.get_all_planes()
        for plane in planes:
            display_name = plane.get('Nickname', plane.get('nickname', f"Plane {plane.get('Id', plane.get('id'))}"))
            plane_id = plane.get('Id', plane.get('id'))
            self.plane_input.addItem(display_name, plane_id)
        
        left_layout.addWidget(plane_label)
        left_layout.addWidget(self.plane_input)

        # Departure airport
        dep_label = QLabel("Departure Airport")
        dep_label.setProperty("class", "fieldLabel")
        self.departure_airport = QComboBox()
        airports = self.airport_controller.get_all_airports()
        for airport in airports:
            display_name = f"{airport.get('Code', airport.get('code', 'UNK'))} - {airport.get('Name', airport.get('name', 'Unknown'))}"
            airport_id = airport.get('Id', airport.get('id'))
            self.departure_airport.addItem(display_name, airport_id)
            
        left_layout.addWidget(dep_label)
        left_layout.addWidget(self.departure_airport)

        # Departure time
        dep_time_label = QLabel("Departure Time")
        dep_time_label.setProperty("class", "fieldLabel")
        self.departure_time = QDateTimeEdit()
        self.departure_time.setCalendarPopup(True)
        self.departure_time.setDateTime(QDateTime.currentDateTime())
        
        left_layout.addWidget(dep_time_label)
        left_layout.addWidget(self.departure_time)

        form_layout.addWidget(left_column)

        # Right column
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(15)

        # Price
        price_label = QLabel("Price (USD)")
        price_label.setProperty("class", "fieldLabel")
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("$")
        self.price_input.setRange(0, 50000)
        self.price_input.setDecimals(2)
        self.price_input.setValue(299.99)
        
        right_layout.addWidget(price_label)
        right_layout.addWidget(self.price_input)

        # Arrival airport
        arr_label = QLabel("Arrival Airport")
        arr_label.setProperty("class", "fieldLabel")
        self.arrival_airport = QComboBox()
        for airport in airports:
            display_name = f"{airport.get('Code', airport.get('code', 'UNK'))} - {airport.get('Name', airport.get('name', 'Unknown'))}"
            airport_id = airport.get('Id', airport.get('id'))
            self.arrival_airport.addItem(display_name, airport_id)
            
        right_layout.addWidget(arr_label)
        right_layout.addWidget(self.arrival_airport)

        # Arrival time
        arr_time_label = QLabel("Arrival Time")
        arr_time_label.setProperty("class", "fieldLabel")
        self.arrival_time = QDateTimeEdit()
        self.arrival_time.setCalendarPopup(True)
        self.arrival_time.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # +1 hour
        
        right_layout.addWidget(arr_time_label)
        right_layout.addWidget(self.arrival_time)

        form_layout.addWidget(right_column)
        content_layout.addLayout(form_layout)

        # Populate form if updating
        if flight:
            self.populate_update_form(flight)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "cancelButton")
        cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cancel_btn.clicked.connect(self.close_form)
        
        submit_btn = QPushButton("Update Flight" if flight else "Create Flight")
        submit_btn.setProperty("class", "formButton")
        submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        if flight:
            submit_btn.clicked.connect(lambda: self.update_flight(flight))
        else:
            submit_btn.clicked.connect(self.submit_flight)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(submit_btn)
        content_layout.addLayout(button_layout)

        main_layout.addWidget(content_widget)
        return form

    def populate_update_form(self, flight):
        """Populate form fields when updating a flight"""
        # Set plane
        for i in range(self.plane_input.count()):
            if self.plane_input.itemData(i) == flight.planeId:
                self.plane_input.setCurrentIndex(i)
                break

        # Set airports
        for i in range(self.departure_airport.count()):
            if self.departure_airport.itemData(i) == flight.departureAirportId:
                self.departure_airport.setCurrentIndex(i)
                break
                
        for i in range(self.arrival_airport.count()):
            if self.arrival_airport.itemData(i) == flight.arrivalAirportId:
                self.arrival_airport.setCurrentIndex(i)
                break

        # Set times
        try:
            dep_time = QDateTime.fromString(flight.departureTime, Qt.ISODate)
            arr_time = QDateTime.fromString(flight.arrivalTime, Qt.ISODate)
            self.departure_time.setDateTime(dep_time)
            self.arrival_time.setDateTime(arr_time)
        except:
            pass  # Use default times if parsing fails

        # Set price
        self.price_input.setValue(flight.price)

    def close_form(self):
        """Close the current form"""
        if self.current_form:
            self.current_form.deleteLater()
            self.current_form = None
            self.add_button.setText("+ Add New Flight")

    def submit_flight(self):
        """Submit new flight"""
        try:
            flight_data = {
                "PlaneId": self.plane_input.currentData(),
                "DepartureAirportId": self.departure_airport.currentData(),
                "ArrivalAirportId": self.arrival_airport.currentData(),
                "DepartureTime": self.departure_time.dateTime().toString(Qt.ISODate),
                "ArrivalTime": self.arrival_time.dateTime().toString(Qt.ISODate),
                "Price": float(self.price_input.value()),
            }
            
            # Validation
            if flight_data["DepartureAirportId"] == flight_data["ArrivalAirportId"]:
                QMessageBox.warning(self, "Error", "Departure and arrival airports cannot be the same.")
                return
            
            if self.departure_time.dateTime() >= self.arrival_time.dateTime():
                QMessageBox.warning(self, "Error", "Arrival time must be after departure time.")
                return

            success = self.flight_controller.create_flight(flight_data)
            if success:
                QMessageBox.information(self, "Success", "Flight created successfully!")
                self.close_form()
                self.load_flights()
            else:
                QMessageBox.warning(self, "Error", "Failed to create flight.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error creating flight: {str(e)}")

    def update_flight(self, flight):
        """Update existing flight"""
        try:
            updated_data = {
                "Id": flight.id,
                "PlaneId": self.plane_input.currentData(),
                "DepartureAirportId": self.departure_airport.currentData(),
                "ArrivalAirportId": self.arrival_airport.currentData(),
                "DepartureTime": self.departure_time.dateTime().toString(Qt.ISODate),
                "ArrivalTime": self.arrival_time.dateTime().toString(Qt.ISODate),
                "Price": float(self.price_input.value()),
            }
            
            # Validation
            if updated_data["DepartureAirportId"] == updated_data["ArrivalAirportId"]:
                QMessageBox.warning(self, "Error", "Departure and arrival airports cannot be the same.")
                return
            
            if self.departure_time.dateTime() >= self.arrival_time.dateTime():
                QMessageBox.warning(self, "Error", "Arrival time must be after departure time.")
                return

            success = self.flight_controller.update_flight(flight.id, updated_data)
            if success:
                QMessageBox.information(self, "Success", "Flight updated successfully!")
                self.close_form()
                self.load_flights()
            else:
                QMessageBox.warning(self, "Error", "Failed to update flight.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error updating flight: {str(e)}")

    def delete_flight(self, flight_id):
        """Delete a flight with confirmation"""
        reply = QMessageBox.question(
            self, 
            "Delete Flight", 
            "Are you sure you want to delete this flight?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.flight_controller.delete_flight(flight_id)
                if success:
                    QMessageBox.information(self, "Success", "Flight deleted successfully!")
                    self.load_flights()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete flight.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error deleting flight: {str(e)}")