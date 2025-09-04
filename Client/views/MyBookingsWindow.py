from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize
from controllers.api_controller import ApiController
from controllers.booking_controller import BookingController
from controllers.flight_controller import FlightController

from services.pdf_service import 

class MyBookingsWindow(QWidget):
    def __init__(self, user_id, parent_screen=None):
        super().__init__()
        self.user_id = user_id
        self.parent_screen = parent_screen
        self.setWindowTitle("My Bookings - IsraFlight")
        self.setWindowIcon(QIcon(r"IsraelFlight_Fronted_6419_6037\Images\logo_icon.png"))
        self.showMaximized()
        self.setStyleSheet("background-color: white; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.create_top_bar())

        title_label = QLabel(f"Your Bookings")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2C3E50; margin: 20px;")
        main_layout.addWidget(title_label)

        self.bookings_table = self.create_bookings_table()
        main_layout.addWidget(self.bookings_table)

        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Arial", 14))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #E74C3C;
                border: 2px solid #E74C3C;
                border-radius: 10px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E74C3C;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn, alignment=Qt.AlignRight)

        main_layout.addWidget(self.create_bottom_bar())

        # Populate bookings table
        self.populate_bookings()

    def create_top_bar(self):
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: white; border-bottom: 2px solid #2980B9;")
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)

        logo = QLabel()
        logo.setPixmap(QIcon("IsraelFlight_Fronted_6419_6037/Images/IsraelFlight_logo.png").pixmap(QSize(150, 150)))
        layout.addWidget(logo, alignment=Qt.AlignLeft)
        return top_bar

    def create_bottom_bar(self):
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("background-color: #34495E;")
        layout = QHBoxLayout(bottom_bar)
        layout.setContentsMargins(20, 10, 20, 10)

        footer_text = QLabel("Version 1.0.3   |   © 2024 Israel Flight   |   support@israelflight.com")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        layout.addWidget(footer_text)
        return bottom_bar

    def create_bookings_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Booking ID", "Flight ID", "Ticket ID", "Booking Date", "PDF"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        return table

    def populate_bookings(self):
        # Filter bookings by user ID
        user_bookings = [b for b in israel_flight_instance.Bookings if b.frequentFlyerId == self.user_id]
        self.bookings_table.setRowCount(len(user_bookings))

        font = QFont()
        font.setBold(True)
        font.setPointSize(10)

        for row, booking in enumerate(user_bookings):
            for col, value in enumerate([
                str(booking.id),
                str(booking.flightId),
                str(getattr(booking, 'ticketId', 'N/A')),
                getattr(booking, 'bookingDate', 'N/A')
            ]):
                item = QTableWidgetItem(value)
                item.setFont(font)
                item.setTextAlignment(Qt.AlignCenter)
                self.bookings_table.setItem(row, col, item)

            pdf_btn = QPushButton()
            pdf_btn.setIcon(QIcon("IsraelFlight_Fronted_6419_6037/Images/PDF.png"))
            pdf_btn.setIconSize(QSize(24, 24))
            pdf_btn.setFixedSize(40, 40)
            pdf_btn.setStyleSheet("border: none; background-color: transparent;")
            pdf_btn.clicked.connect(lambda checked, b=booking: self.generate_pdf(b))
            self.bookings_table.setCellWidget(row, 4, pdf_btn)
            self.bookings_table.setRowHeight(row, 50)

    def generate_pdf(self, booking):
        # Find flight object
        flight = next((f for f in israel_flight_instance.Flights if f.id == booking.flightId), None)
        if not flight:
            QMessageBox.critical(self, "Error", "Flight not found for this booking.")
            return

        ticket = Ticket(
            Id=getattr(booking, 'ticketId', 0),
            BookingId=booking.id,
            FlightId=booking.flightId,
            Seat=getattr(booking, 'seat', 'N/A'),
            PdfUrl='url'
        )
        file_path = f"IsraelFlight_Fronted_6419_6037/PDF_files/ticket_{booking.id}.pdf"
        create_ticket_pdf(ticket, file_path, self.user_id)

        QMessageBox.information(self, "PDF Created", f"PDF created successfully at:\n{file_path}")
