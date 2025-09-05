from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QFrame, QGraphicsDropShadowEffect, QGridLayout
)
from PySide6.QtGui import QCursor, QPainter, QPainterPath
from PySide6.QtCore import Qt

from controllers.api_controller import ApiController
from controllers.flight_controller import FlightController
from controllers.booking_controller import BookingController
from controllers.airport_controller import AirportController
from views.bookaflight import BookFlightWindow
from views.MyBookingsWindow import MyBookingsWindow





class UserWindow(QMainWindow):
    def __init__(self, user_obj):
        super().__init__()
        self.user_id = getattr(user_obj, "Id", None) or getattr(user_obj, "id", None)

        self.setWindowTitle("IsraFlight - User Dashboard")
        self.setFixedSize(1000, 700)

        self.setWindowFlags(Qt.Window)
        self.setup_styling()
        self.init_ui()
       

    def setup_styling(self):
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }

            QFrame#mainFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f9fafb, stop:1 #edf2f7);
                border: 1px solid rgba(226, 232, 240, 0.8);
            }

            QWidget#navBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b6cb0, stop:1 #2c5282);
                border-bottom: 2px solid #2a4365;
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
                border: 1px solid rgba(255, 255, 255, 0.3);
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
            }

            QLabel#welcomeLabel {
                font-size: 22pt;
                font-weight: 300;
                color: #2d3748;
                margin: 20px 0px;
            }

            QLabel#subtitleLabel {
                font-size: 14pt;
                color: #4a5568;
                margin-bottom: 30px;
            }

            QPushButton#actionButton {
                font-size: 14pt;
                font-weight: 600;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 20px 30px;
                min-height: 80px;
                min-width: 200px;
                text-align: center;
            }

            QPushButton#bookFlightButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4299e1, stop:1 #3182ce);
            }

            QPushButton#bookFlightButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3182ce, stop:1 #2b6cb0);
            }

            QPushButton#myBookingsButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
            }

            QPushButton#myBookingsButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #38a169, stop:1 #2f855a);
            }
        """)

    def init_ui(self):
        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_frame)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 15)
        self.main_frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # NavBar
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(70)

        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 15, 30, 15)

        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))

        lbl_title = QLabel("User Dashboard")
        lbl_title.setObjectName("titleLabel")
        lbl_brand = QLabel("IsraFlight")
        lbl_brand.setObjectName("brandLabel")

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch(1)
        nav_layout.addWidget(lbl_title)
        nav_layout.addStretch(1)
        nav_layout.addWidget(lbl_brand)

        layout.addWidget(nav_bar)

        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 40, 50, 50)
        content_layout.setSpacing(30)

        welcome = QLabel(f"Welcome back, User #{self.user_id}")
        welcome.setObjectName("welcomeLabel")
        welcome.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome)

        subtitle = QLabel("Book your next flight or view your bookings")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(45)

        # Book Flight Button
        self.btn_book_flight = self.create_action_button(
            "✈️", "Book a Flight", "Browse flights and reserve your flight", "bookFlightButton"
        )

        # My Bookings Button
        self.btn_my_bookings = self.create_action_button(
            "🧾", "My Bookings", "View and manage your reservations", "myBookingsButton"
        )

        grid.addWidget(self.btn_book_flight, 0, 0)
        grid.addWidget(self.btn_my_bookings, 0, 1)

        content_layout.addLayout(grid)
        content_layout.addStretch()
        layout.addWidget(content)

        # Connect actions
        self.btn_back.clicked.connect(self.close)
        self.btn_book_flight.clicked.connect(self.on_book_flight)
        self.btn_my_bookings.clicked.connect(self.on_my_bookings)

    def create_action_button(self, icon, title, desc, style_class):
        button = QPushButton()
        button.setObjectName("actionButton")
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setMinimumSize(250, 120)

        inner = QVBoxLayout(button)
        inner.setContentsMargins(20, 20, 20, 20)
        inner.setSpacing(6)

        lbl_icon = QLabel(icon)
        lbl_icon.setAlignment(Qt.AlignCenter)
        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_desc = QLabel(desc)
        lbl_desc.setAlignment(Qt.AlignCenter)
        lbl_desc.setWordWrap(True)

        inner.addWidget(lbl_icon)
        inner.addWidget(lbl_title)
        inner.addWidget(lbl_desc)

        button.setProperty("class", style_class)
        button.setObjectName(style_class)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        button.setGraphicsEffect(shadow)

        return button

    def on_book_flight(self):
        self.book_flight_window = BookFlightWindow(self.user_id)
        self.book_flight_window.show()
        print("🛫 Book Flight clicked")


    def on_my_bookings(self):
        api = ApiController(base_url="http://localhost:5126/api")
        self.my_bookings_window = MyBookingsWindow(self.user_id, api)
        self.my_bookings_window.show()


        print("🧾 My Bookings clicked")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.fillPath(path, Qt.transparent)
        super().paintEvent(event)
