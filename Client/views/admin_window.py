from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsDropShadowEffect, QGridLayout
)
from PySide6.QtGui import QFont, QCursor, QPainter, QPainterPath, QIcon
from PySide6.QtCore import Qt

from controllers.api_controller import ApiController

from controllers.plane_controller import PlaneController
from .plane_window import PlaneWindow

from controllers.flight_controller import FlightController
from .flight_window import FlightWindow

from controllers.airport_controller import AirportController


class AdminWindow(QMainWindow):
    def __init__(self, admin_controller):
        super().__init__()
        self.admin_controller = admin_controller
        self.setWindowTitle("IsraFlight - Admin Dashboard")
        self.setFixedSize(1200, 800)
        
        # Modern window styling
        self.setWindowFlags(Qt.Window)  
        
        self.setup_styling()
        self.init_ui()
    
    def setup_styling(self):
        """Setup professional admin panel styling"""
        self.setStyleSheet("""
            QMainWindow {
                background: transparent;
            }
            
            QFrame#mainFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc, stop:1 #e2e8f0);
                border: 1px solid rgba(226, 232, 240, 0.8);
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
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            QLabel#titleLabel {
                font-size: 20pt;
                font-weight: bold;
                color: white;
                background: transparent;
            }
            
            QLabel#brandLabel {
                font-weight: bold;
                color: white;
                font-size: 16pt;
                background: transparent;
                letter-spacing: 1px;
            }
            
            QLabel#welcomeLabel {
                font-size: 24pt;
                font-weight: 300;
                color: #2d3748;
                background: transparent;
                margin: 20px 0px;
            }
            
            QLabel#subtitleLabel {
                font-size: 14pt;
                color: #718096;
                background: transparent;
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
                text-align: left;
            }
            
            QPushButton#planesButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            
            QPushButton#planesButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            
            QPushButton#flightsButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #48bb78, stop:1 #38a169);
            }
            
            QPushButton#flightsButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #38a169, stop:1 #2f855a);
            }
            
            QLabel#iconLabel {
                font-size: 32pt;
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
            
            QLabel#buttonTitle {
                font-size: 16pt;
                font-weight: bold;
                color: white;
                background: transparent;
            }
            
            QLabel#buttonDesc {
                font-size: 11pt;
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
            }
        """)
    
    def init_ui(self):
        """Initialize professional admin UI"""
        # Main container frame
        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")

        # Create a central widget and layout for the QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_frame)
        
        # Add professional drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 15)
        self.main_frame.setGraphicsEffect(shadow)
        
        # Main layout
        main_layout = QVBoxLayout(self.main_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === Navigation Bar ===
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(80)
        
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 20, 30, 20)
        
        # Back button with modern styling
        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Title
        lbl_title = QLabel("Admin Dashboard")
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
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(50, 40, 50, 50)
        content_layout.setSpacing(30)
        
        # Welcome section
        welcome_label = QLabel("Welcome to Admin Control")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome_label)
        
        subtitle_label = QLabel("Manage your airline operations efficiently")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(subtitle_label)
        
        # === Action Buttons Grid ===
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(45)
        
        # Planes Management Button
        self.btn_planes = self.create_action_button(
            "✈️", "Planes Management", 
            "View and manage your fleet of aircraft",
            "planesButton"
        )
        
        # Flights Management Button  
        self.btn_flights = self.create_action_button(
            "🛫", "Flight Operations",
            "Schedule and manage flight operations", 
            "flightsButton"
        )
        
        
        # Arrange in 2x2 grid
        buttons_layout.addWidget(self.btn_planes, 0, 0)
        buttons_layout.addWidget(self.btn_flights, 0, 1)
    
        
        content_layout.addLayout(buttons_layout)
        content_layout.addStretch()
        
        main_layout.addWidget(content_widget)
        
        # === Connect Signals ===
        self.btn_back.clicked.connect(self.close)
        self.btn_planes.clicked.connect(self.on_planes_clicked)
        self.btn_flights.clicked.connect(self.on_flights_clicked)
    
    def create_action_button(self, icon, title, description, style_class):
        """Create a modern action button with icon and description"""
        button = QPushButton()
        button.setObjectName("actionButton")
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setMinimumSize(250, 120)
        
        # Create button layout
        button_layout = QVBoxLayout(button)
        button_layout.setContentsMargins(20, 20, 20, 20)
        button_layout.setSpacing(6)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setObjectName("iconLabel")
        icon_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("buttonTitle")
        title_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setObjectName("buttonDesc")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        button_layout.addWidget(desc_label)
        
        # Button styling 
        button.setStyleSheet("""
            QPushButton#actionButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
            }
            QPushButton#actionButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
        """ + self.styleSheet())
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(Qt.darkGray)
        shadow.setOffset(0, 5)
        button.setGraphicsEffect(shadow)
        
        return button
    
    def on_planes_clicked(self):
        api = ApiController(base_url="http://localhost:5126/api")
        planes_controller = PlaneController(api)
        planes_view = PlaneWindow(planes_controller, self)
        planes_view.show()
            
    def on_flights_clicked(self):
        api = ApiController(base_url="http://localhost:5126/api")
        flight_ctrl = FlightController(api)
        plane_ctrl = PlaneController(api)
        airport_ctrl = AirportController(api)
        flight_view = FlightWindow(flight_ctrl, plane_ctrl, airport_ctrl, self)
        flight_view.show()
        
    
    def paintEvent(self, event):
        """Custom paint event for modern appearance"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        
        # Fill with semi-transparent background
        painter.fillPath(path, Qt.transparent)
        
        super().paintEvent(event)