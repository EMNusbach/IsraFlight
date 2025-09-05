from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect, QFrame, QDateEdit, QApplication
)
from PySide6.QtGui import QFont, QCursor, QPainter, QPainterPath
from PySide6.QtCore import Qt, QDate

from controllers.frequentFlyer_controller import FrequentFlyerController
from models import FrequentFlyer

class RegisterDialog(QDialog):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Register - IsraFlight")
        self.setModal(True)
        self.setFixedSize(500, 750)  # Made shorter to fit better
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.api = api 
        self.frequentFlyer_controller = FrequentFlyerController(self.api)
        
        
        # Center the dialog on screen
        self.center_on_screen()
        
        self.setup_styling()
        self.init_ui()

    def center_on_screen(self):
        """Center the dialog on the screen, with optional offset"""
        offset_x = -160  # Move 100px to the left
        if self.parent():
            # Center relative to parent
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2 + offset_x
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
        else:
            # Center on screen
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2 + offset_x
            y = (screen.height() - self.height()) // 2

        self.move(x, y)


    def setup_styling(self):
        self.setStyleSheet("""

            QFrame#mainFrame {
                background: rgba(255, 255, 255, 1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
            }

            QLabel#titleLabel {
                font-size: 24pt;
                font-weight: bold;
                color: #1a202c;
                background: transparent;
                margin: 0px;
                min-height: 40px;
            }

            QLabel#subtitleLabel {
                font-size: 12pt;
                color: #718096;
                background: transparent;
                margin: 0px;
                padding: 2px;
            }

            QLineEdit, QDateEdit {
                padding: 10px 16px;  
                font-size: 11pt;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background: white;
                color: #2d3748;
                selection-background-color: #4a5568;
                min-height: 15px;
            }

            QLineEdit:focus, QDateEdit:focus {
                border: 2px solid #4a5568;
                background: #f7fafc;
            }

            QPushButton#registerButton {
                font-size: 12pt;
                font-weight: 600;
                color: white;
                border: none;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                padding: 12px 24px;
                min-height: 35px;
                max-height: 45px;
            }

            QPushButton#registerButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }

            QPushButton#closeButton {
                background: transparent;
                border: none;
                color: #718096;
                font-size: 18pt;
                font-weight: bold;
                border-radius: 20px;
                padding: 8px;
                min-width: 40px;
                min-height: 40px;
            }

            QPushButton#closeButton:hover {
                background: rgba(226, 232, 240, 0.8);
                color: #2d3748;
            }
        """)

    def init_ui(self):
        # Main frame - adjusted size and position
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("mainFrame")
        self.main_frame.setGeometry(20, 70, 460, 660)  # Centered better with more space
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 10)
        self.main_frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(25, 10, 25, 20)  # Reduced margins
        layout.setSpacing(10)  

        # Close button
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        self.close_btn = QPushButton("×", self.main_frame)
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.clicked.connect(self.reject)
        header_layout.addWidget(self.close_btn)
        layout.addLayout(header_layout)

        # Title
        title = QLabel("Join IsraFlight!", self.main_frame)
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Create your frequent flyer account", self.main_frame)
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        layout.addSpacing(15)  # Reduced spacing

        # Input fields
        self.username_input = QLineEdit(self.main_frame)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self.main_frame)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.firstname_input = QLineEdit(self.main_frame)
        self.firstname_input.setPlaceholderText("First Name")
        layout.addWidget(self.firstname_input)

        self.lastname_input = QLineEdit(self.main_frame)
        self.lastname_input.setPlaceholderText("Last Name")
        layout.addWidget(self.lastname_input)

        self.email_input = QLineEdit(self.main_frame)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.phone_input = QLineEdit(self.main_frame)
        self.phone_input.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_input)

        self.dob_input = QDateEdit(self.main_frame)
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        layout.addWidget(self.dob_input)

        self.passport_input = QLineEdit(self.main_frame)
        self.passport_input.setPlaceholderText("Passport Number")
        layout.addWidget(self.passport_input)
        layout.addSpacing(10)  # Space before button

        # Register button
        self.register_btn = QPushButton("Register", self.main_frame)
        self.register_btn.setObjectName("registerButton")
        self.register_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_btn.clicked.connect(self.handle_register)
        layout.addWidget(self.register_btn)

        
        # Small stretch at the bottom to push everything up slightly
        layout.addSpacing(15)

    def handle_register(self):
        # Collect and trim all input values
        flyer = {
            "Username": self.username_input.text().strip(),
            "Password": self.password_input.text().strip(),
            "FirstName": self.firstname_input.text().strip(),
            "LastName": self.lastname_input.text().strip(),
            "Email": self.email_input.text().strip(),
            "PhoneNumber": self.phone_input.text().strip(),
            "DateOfBirth": self.dob_input.date().toPython().isoformat(),
            "PassportNumber": self.passport_input.text().strip()
        }

        # Check for empty fields
        missing_fields = [key for key, value in flyer.items() if not value]
        if missing_fields:
            field_names = ", ".join(missing_fields)
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Missing Fields")
            msg_box.setText(f"Please fill in all the fields.\nMissing: {field_names}")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            return  # Stop registration

        result = self.frequentFlyer_controller.register(flyer)

        if result["success"]:
            # Success message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Success")
            msg_box.setText("Registration successful!")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            self.accept()
        else:
            # Failure - show the exact error from the backend
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"Registration failed:\n{result['error']}")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.fillPath(path, Qt.transparent)
        super().paintEvent(event)