from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QLineEdit, QDateEdit, QSpinBox, QComboBox, QMessageBox, QScrollArea,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import QDate, Qt, QDateTime
from PySide6.QtGui import QCursor
from datetime import datetime
from fpdf import FPDF

from controllers.airport_controller import AirportController
from controllers.api_controller import ApiController
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from models import Flight, Airport


class BookFlightWindow(QMainWindow):
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

        self.setWindowTitle("Book a Flight - IsraFlight")
        self.setFixedSize(1200, 800)

        # --- Central Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Navigation Bar ---
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(80)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 20, 30, 20)

        btn_back = QPushButton("←")
        btn_back.setObjectName("backButton")
        btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        btn_back.clicked.connect(self.close)

        lbl_title = QLabel("✈️ Book a Flight")
        lbl_title.setObjectName("titleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_brand = QLabel("IsraFlight")
        lbl_brand.setObjectName("brandLabel")
        lbl_brand.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(btn_back)
        nav_layout.addStretch()
        nav_layout.addWidget(lbl_title)
        nav_layout.addStretch()
        nav_layout.addWidget(lbl_brand)
        main_layout.addWidget(nav_bar)

        # --- Content Area ---
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(30)
        main_layout.addWidget(content_widget)

        # Search Form Section
        form_section = self.create_search_form()
        content_layout.addWidget(form_section,0)

        # Results Section
        self.results_section = self.create_results_section()
        self.results_section.hide()
        content_layout.addWidget(self.results_section,1)

        # Apply styles
        self.setStyleSheet(self.get_stylesheet())

    def create_search_form(self):
        """Create a compact airline-style flight search bar"""
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QHBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        airport_names = [f"{a.city} ({a.code})" for a in self.airports]

        # From Airport
        from_label = QLabel("From")
        from_label.setObjectName("fieldLabel")
        self.from_input = QComboBox()
        self.from_input.setObjectName("formField")
        self.from_input.addItems(airport_names)

        # To Airport
        to_label = QLabel("To")
        to_label.setObjectName("fieldLabel")
        self.to_input = QComboBox()
        self.to_input.setObjectName("formField")
        self.to_input.addItems(airport_names)

        # Departure Date
        date_label = QLabel("Date")
        date_label.setObjectName("fieldLabel")
        self.date_input = QDateEdit()
        self.date_input.setObjectName("formField")
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        # Passengers
        passengers_label = QLabel("Pax")
        passengers_label.setObjectName("fieldLabel")
        self.passengers_input = QSpinBox()
        self.passengers_input.setObjectName("formField")
        self.passengers_input.setMinimum(1)
        self.passengers_input.setMaximum(9)
        self.passengers_input.setValue(1)

        # Class
        class_label = QLabel("Class")
        class_label.setObjectName("fieldLabel")
        self.class_input = QComboBox()
        self.class_input.setObjectName("formField")
        self.class_input.addItems(["Economy", "Premium Economy", "Business", "First Class"])

        # Search Button
        search_btn = QPushButton("🔍 Search")
        search_btn.setObjectName("searchButton")
        search_btn.setCursor(QCursor(Qt.PointingHandCursor))
        search_btn.clicked.connect(self.search_flights)

        # Add widgets to layout (all in one row)
        for w in [
            from_label, self.from_input,
            to_label, self.to_input,
            date_label, self.date_input,
            passengers_label, self.passengers_input,
            class_label, self.class_input,
            search_btn
        ]:
            form_layout.addWidget(w)

        return form_container

    def create_results_section(self):
        """Create the results section"""
        results_container = QWidget()
        results_layout = QVBoxLayout(results_container)
        results_layout.setContentsMargins(0, 0, 0, 0)
        results_layout.setSpacing(20)

        # Results Header
        header_layout = QVBoxLayout()
        results_title = QLabel("Available Flights")
        results_title.setObjectName("resultsTitle")
        results_subtitle = QLabel("Choose your preferred flight")
        results_subtitle.setObjectName("resultsSubtitle")
        header_layout.addWidget(results_title)
        header_layout.addWidget(results_subtitle)
        results_layout.addLayout(header_layout)

        # Flights Scroll Area
        self.flights_scroll = QScrollArea()
        self.flights_scroll.setWidgetResizable(True)
        self.flights_scroll.setObjectName("flightsScrollArea")
        self.flights_container = QWidget()
        self.flights_layout = QVBoxLayout(self.flights_container)
        self.flights_layout.setSpacing(12)
        self.flights_layout.setContentsMargins(0, 0, 0, 0)
        self.flights_scroll.setWidget(self.flights_container)
        self.flights_scroll.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        
        results_container.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )


        results_layout.addWidget(self.flights_scroll)
        

        return results_container

    def search_flights(self):
        """Search flights based on form input"""
        from_id = self.get_airport_id(self.from_input)
        to_id = self.get_airport_id(self.to_input)
        departure_date = self.date_input.date().toPython()

        if from_id == -1 or to_id == -1 or from_id == to_id:
            QMessageBox.warning(self, "Validation Error", "Please select valid departure and destination airports")
            return

        flights = self.flight_ctrl.get_all_flights()
        matched = [
            f for f in flights
            if f.departureAirportId == from_id
            and f.arrivalAirportId == to_id
            and datetime.fromisoformat(f.departureTime).date() == departure_date
        ]

        if not matched:
            matched = flights
            QMessageBox.information(self, "No Exact Matches", "No flights match your criteria. Showing all available flights.")

        # Clear old results
        for i in reversed(range(self.flights_layout.count())):
            widget = self.flights_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add new flight cards
        for f in matched:
            flight_card = self.create_flight_card(f)
            self.flights_layout.addWidget(flight_card)
        self.flights_layout.addStretch()

        # Show results section
        self.results_section.show()

        # ✅ Scroll to the top of the results
        self.flights_scroll.verticalScrollBar().setValue(0)


    def create_flight_card(self, flight: Flight):
        """Create a modern flight card"""
        card = QFrame()
        card.setObjectName("flightCard")
        
        card.setMinimumHeight(160)   # adjust as you like
        card.setMaximumHeight(160)   # lock height so it doesn’t shrink
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Main card layout
        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top section with flight info
        top_section = QWidget()
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(24, 20, 24, 16)
        top_layout.setSpacing(20)
        
        # Left: Flight Info
        left_side = QWidget()
        left_layout = QVBoxLayout(left_side)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        flight_info = QLabel(f"IsraFlight • Flight {flight.id}")
        flight_info.setStyleSheet("""
            font-size: 11pt;
            color: #1a202c;
            font-weight: bold;
        """)
        left_layout.addWidget(flight_info)
        
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
        
        dep_code_label = QLabel(str(flight.departureAirportId))
        dep_code_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #1a202c;
        """)
        dep_city_label = QLabel(self.get_airport_name(flight.departureAirportId))
        dep_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        dep_time_label = QLabel(datetime.fromisoformat(flight.departureTime).strftime('%H:%M'))
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

        arr_code_label = QLabel(str(flight.arrivalAirportId))
        arr_code_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #1a202c;
        """)
        arr_city_label = QLabel(self.get_airport_name(flight.arrivalAirportId))
        arr_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        arr_time_label = QLabel(datetime.fromisoformat(flight.arrivalTime).strftime('%H:%M'))
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

        # Aircraft info
        if hasattr(flight, 'plane') and flight.plane:
            plane_info = QLabel(f"Aircraft: {getattr(flight.plane, 'name', 'Unknown')}")
        else:
            plane_info = QLabel("Aircraft: Unknown")
        plane_info.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        center_layout.addWidget(plane_info)

        # Right side - Price and book button
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignTop)

        # Price
        price_label = QLabel(f"${flight.price:,.2f}")
        price_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #1a202c;
        """)
        price_label.setAlignment(Qt.AlignRight)
        right_layout.addWidget(price_label)

        # Book button
        book_btn = QPushButton("Book Flight")
        book_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #48bb78, stop:1 #38a169);
                color: white;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38a169, stop:1 #2f855a);
            }
        """)
        book_btn.setCursor(QCursor(Qt.PointingHandCursor))
        book_btn.clicked.connect(lambda: self.book_flight(flight))
        right_layout.addWidget(book_btn)

        # Add all sections to top layout
        top_layout.addWidget(left_side)
        top_layout.addWidget(center_section)
        top_layout.addWidget(right_side)
        
        # Add top section to main card layout
        main_layout.addWidget(top_section)

        return card

    def get_airport_name(self, airport_id):
        """Get airport name from ID"""
        for a in self.airports:
            if a.id == airport_id:
                return f"{a.city} ({a.code})"
        return str(airport_id)

    def get_airport_id(self, combo: QComboBox):
        """Get airport ID from combo selection"""
        index = combo.currentIndex()
        if 0 <= index < len(self.airports):
            return self.airports[index].id
        return -1

    def book_flight(self, flight: Flight):
        """Book the selected flight"""
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

    def generate_pdf_ticket(self, booking):
        """Generate PDF ticket"""
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

    def get_stylesheet(self):
        return """
            QMainWindow { background-color: #f8fafc; }
            QWidget#contentWidget { background-color: #f8fafc; }
            
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
            QPushButton#backButton:hover { background: rgba(255, 255, 255, 0.2); }
            
            QLabel#titleLabel { font-size: 20pt; font-weight: bold; color: white; }
            QLabel#brandLabel { font-weight: bold; color: white; font-size: 16pt; letter-spacing: 1px; min-width: 120px; }
            
            QFrame#formContainer {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            
            QLabel#formTitle { font-size: 24pt; font-weight: bold; color: #1a202c; }
            QLabel#formSubtitle { font-size: 14pt; color: #718096; }
            
            QLabel#fieldLabel {
                font-size: 12pt;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 5px;
            }
            
            QComboBox#formField {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 10pt;
                background-color: white;
                min-width: 110px;   /* narrower */
                min-height: 28px;   /* shorter */
            }

            QComboBox#formField::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #e2e8f0;
                border-radius: 0 8px 8px 0;
                background-color: #f1f5f9;
            }

            QComboBox#formField::down-arrow {
                image: url(:/icons/arrow-down.svg); /* optional custom arrow */
                width: 10px;
                height: 10px;
            }

            QComboBox#formField:hover {
                border: 1px solid #3182ce;
                background-color: #f0f9ff;
            }

            QComboBox#formField:focus {
                border: 2px solid #3182ce;
                background-color: #ffffff;
            }


            
            QPushButton#searchButton {
                background-color: #3182ce;
                color: white;
                padding: 8px 20px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                min-width: 120px;
            }
            QPushButton#searchButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b6cb0, stop:1 #2a4365);
            }
            
            QLabel#resultsTitle { font-size: 20pt; font-weight: bold; color: #1a202c; }
            QLabel#resultsSubtitle { font-size: 12pt; color: #718096; }
            
            QScrollArea#flightsScrollArea { border: none; background-color: transparent; }
            QScrollArea#flightsScrollArea QScrollBar:vertical {
                border: none; background-color: #f1f5f9; width: 12px; border-radius: 6px;
            }
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical {
                background-color: #cbd5e1; border-radius: 6px; min-height: 20px;
            }
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical:hover { background-color: #94a3b8; }
            
            QFrame#flightCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#flightCard:hover {
                border-color: #cbd5e1;
                background: #fefefe;
            }
        """