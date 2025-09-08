from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGraphicsDropShadowEffect, QMessageBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QCursor
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController
from controllers.airport_controller import AirportController
from controllers.frequentFlyer_controller import FrequentFlyerController
from services.pdf_service import generate_ticket_pdf
import os, webbrowser

class MyBookingsWindow(QMainWindow):
    def __init__(self, user_id, api):
        super().__init__()
        self.user_id = user_id
        self.booking_controller = BookingController(api)
        self.flight_controller = FlightController(api)
        self.airport_controller = AirportController(api)

        self.setWindowTitle("My Bookings - IsraFlight")
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

        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.clicked.connect(self.close)

        lbl_title = QLabel("🧾 My Bookings")
        lbl_title.setObjectName("titleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_brand = QLabel("IsraFlight")
        lbl_brand.setObjectName("brandLabel")
        lbl_brand.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        nav_layout.addWidget(lbl_title)
        nav_layout.addStretch()
        nav_layout.addWidget(lbl_brand)
        main_layout.addWidget(nav_bar)

        # --- Content Area ---
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)
        main_layout.addWidget(content_widget)

        # Header
        header_section = QWidget()
        header_layout = QHBoxLayout(header_section)
        header_layout.setContentsMargins(0, 0, 0, 0)

        main_title = QLabel("Your Flight Bookings")
        main_title.setObjectName("mainTitle")
        subtitle = QLabel("Manage and download your tickets")
        subtitle.setObjectName("subtitle")

        title_layout = QVBoxLayout()
        title_layout.addWidget(main_title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        self.main_layout.addWidget(header_section)

        # --- Bookings Scroll Area ---
        self.bookings_area = QScrollArea()
        self.bookings_area.setWidgetResizable(True)
        self.bookings_area.setObjectName("flightsScrollArea")
        self.bookings_container = QWidget()
        self.bookings_layout = QVBoxLayout(self.bookings_container)
        self.bookings_layout.setSpacing(12)
        self.bookings_layout.setContentsMargins(0, 0, 0, 0)
        self.bookings_area.setWidget(self.bookings_container)
        self.main_layout.addWidget(self.bookings_area)

        # Load bookings
        self.load_bookings()

        # Apply styles
        self.setStyleSheet(self.get_stylesheet())

    def create_booking_card(self, booking, flight):
        """Create a modern booking card"""
        dep_airport = self.get_airport_name(flight.departureAirportId)
        arr_airport = self.get_airport_name(flight.arrivalAirportId)

        card = QFrame()
        card.setObjectName("bookingCard")
        card.setMinimumHeight(200)

                
        # Main card layout
        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top section with flight info
        top_section = QWidget()
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(24, 20, 24, 16)
        top_layout.setSpacing(20)
        
        # --- Left: Flight Info ---
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
        dep_city_label = QLabel(dep_airport)
        dep_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        dep_time_label = QLabel(str(flight.departureTime)) 
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
        arr_city_label = QLabel(arr_airport)
        arr_city_label.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
        """)
        arr_time_label = QLabel(str(flight.arrivalTime)) 
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

        

        # Right side - Price and actions
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignTop)

        # Price
        price_label = QLabel(f"Price: ${getattr(flight, 'price', 'N/A')}")
        price_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #1a202c;
        """)
        price_label.setAlignment(Qt.AlignRight)
        right_layout.addWidget(price_label)

        # PDF Download button
        pdf_btn = QPushButton("📄 Download PDF")
        pdf_btn.setProperty("class", "pdfButton")
        pdf_btn.setCursor(QCursor(Qt.PointingHandCursor))
        pdf_btn.clicked.connect(lambda _, b=booking: self.generate_pdf(b))
        pdf_btn.setStyleSheet("""
            QPushButton {
                background: #e2e8f0;
                color: #1a202c;
                padding: 6px 12px;
                font-size: 10pt;
                border-radius: 6px;
                border: none;
                margin-bottom: 8px;
            }
            QPushButton:hover {
                background: #cbd5e1;
            }
        """)
        right_layout.addWidget(pdf_btn)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

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
        delete_btn.clicked.connect(lambda _, b=booking: self.delete_flight(b.id))

        button_layout.addWidget(delete_btn)
        right_layout.addLayout(button_layout)

        # Add all sections to top layout
        top_layout.addWidget(left_side)
        top_layout.addWidget(center_section)
        top_layout.addWidget(right_side)
        
        # Add top section to main card layout
        main_layout.addWidget(top_section)

        return card

    def get_airport_name(self, airport_id):
        airports = self.airport_controller.get_all_airports()
        for a in airports:
            if a.get("id") == airport_id:
                return a.get("name")
        return "Unknown Airport"

    def generate_pdf(self, booking):
        """Generate PDF ticket and open it safely"""
        try:
            flight = self.flight_controller.get_flight_by_id(booking.flightId)
        except Exception:
            QMessageBox.warning(self, "Error", "Flight not found")
            return

        ff_controller = FrequentFlyerController(self.booking_controller.api)
        traveler_name = ff_controller.get_full_name(self.user_id)
        dep_airport = self.get_airport_name(flight.departureAirportId)
        arr_airport = self.get_airport_name(flight.arrivalAirportId)

        try:
            pdf_path = generate_ticket_pdf(
                booking, flight,
                traveler_name=traveler_name,
                dep_airport_name=dep_airport,
                arr_airport_name=arr_airport
            )
            if pdf_path and os.path.exists(pdf_path):
                webbrowser.open_new(pdf_path)
            else:
                QMessageBox.warning(self, "Error", "Failed to generate PDF or file not found")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not generate PDF:\n{e}")

    def load_bookings(self):
        """Load all user bookings"""
        bookings = self.booking_controller.list_user_bookings(self.user_id)

        # Clear previous
        for i in reversed(range(self.bookings_layout.count())):
            item = self.bookings_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        if not bookings:
            empty_label = QLabel("No bookings found.")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 18pt; color: #a0aec0; padding: 40px;")
            self.bookings_layout.addWidget(empty_label)
            return

        for booking in bookings:
            try:
                flight = self.flight_controller.get_flight_by_id(booking.flightId)
            except Exception:
                continue
            card = self.create_booking_card(booking, flight)
            self.bookings_layout.addWidget(card)
            
        self.bookings_layout.addStretch()


    # You'll need to implement these methods based on your application logic
    def open_update_form(self, flight):
        """Open update form for the flight"""
        # Implement based on your application needs
        QMessageBox.information(self, "Update", f"Update form for flight {flight.id}")

    def delete_flight(self, booking_id):
        """Delete flight booking"""
        reply = QMessageBox.question(
            self, "Delete Booking",
            "Are you sure you want to delete this booking?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.booking_controller.delete_booking(booking_id)
                QMessageBox.information(self, "Deleted", "Booking deleted successfully")
                self.load_bookings()  # Refresh the list
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete booking:\n{e}")


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
            QLabel#mainTitle { font-size: 24pt; font-weight: bold; color: #1a202c; }
            QLabel#subtitle { font-size: 14pt; color: #718096; }
            QScrollArea#flightsScrollArea { border: none; background-color: transparent; }
            QScrollArea#flightsScrollArea QScrollBar:vertical {
                border: none; background-color: #f1f5f9; width: 12px; border-radius: 6px;
            }
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical {
                background-color: #cbd5e1; border-radius: 6px; min-height: 20px;
            }
            QScrollArea#flightsScrollArea QScrollBar::handle:vertical:hover { background-color: #94a3b8; }
            QFrame#bookingCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#bookingCard:hover {
                border-color: #cbd5e1;
                background: #fefefe;
            }
        """