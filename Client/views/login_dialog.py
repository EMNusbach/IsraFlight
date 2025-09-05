from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect, QFrame
)
from PySide6.QtGui import QFont, QCursor, QPainter, QPainterPath, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from controllers.auth_controller import AuthController 
from controllers.admin_controller import AdminController
from views.admin_window import AdminWindow
from views.register_dialog import RegisterDialog
from views.user_window import UserWindow


class LoginDialog(QDialog):
    def __init__(self, auth_controller: AuthController, api):
        super().__init__()
        self.setWindowTitle("Sign In - IsraFlight")
        self.setModal(True)
        self.setFixedSize(480, 580)
        
        # Remove default window frame for custom design
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Store references
        self.auth_controller = auth_controller  
        self.api = api 
        
        self.setup_styling()
        self.init_ui()
        self.connect_signals()
        self.add_animations()
        self.user_obj = None  # <-- store logged-in user here

    
    def setup_styling(self):
        """Setup modern styling with dusty blue aesthetic"""
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            
            QFrame#mainFrame {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
            }

            QLabel#titleLabel {
                font-size: 28pt;
                font-weight: bold;
                color: #1a202c;
                background: transparent;
                margin: 0px;
            }

            QLabel#subtitleLabel {
                font-size: 14pt;
                color: #718096;
                background: transparent;
                margin: 0px;
            }

            QLineEdit {
                padding: 16px 20px;
                font-size: 14pt;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background: white;
                color: #2d3748;
                selection-background-color: #4a5568;
            }

            QLineEdit:focus {
                border: 2px solid #4a5568;
                background: #f7fafc;
            }

            QLineEdit::placeholder {
                color: #a0aec0;
            }

            QPushButton#loginButton {
                font-size: 14pt;
                font-weight: 600;
                color: white;
                border: none;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                padding: 16px 24px;
                min-height: 50px;
            }

            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }

            QPushButton#loginButton:pressed {
                background: #1a202c;
            }

            QPushButton#loginButton:disabled {
                background: #cbd5e0;
                color: #a0aec0;
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

            QLabel#infoLabel {
                font-size: 12pt;
                color: #4a5568;
                background: transparent;
            }

            QLabel#linkLabel {
                font-size: 12pt;
                color: #4a5568;
                background: transparent;
                text-decoration: underline;
            }

            QLabel#linkLabel:hover {
                color: #2d3748;
            }
        """)

    
    def init_ui(self):
        """Initialize modern UI layout"""
        # Main container frame with glassmorphism
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("mainFrame")
        self.main_frame.setGeometry(20, 20, 440, 540)
        
        # Add drop shadow to main frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 10)
        self.main_frame.setGraphicsEffect(shadow)
        
        # Layout for main frame content
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(40, 40, 30, 40)
        layout.setSpacing(0)
        
        # === Header with close button ===
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0,20)
        
        # Close button
        self.close_btn = QPushButton("×", self.main_frame)
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.clicked.connect(self.reject)
        
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)

        layout.addLayout(header_layout)
        
        # === Title Section ===
        title = QLabel("Welcome back!", self.main_frame)
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Sign in to access your account", self.main_frame)
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        layout.addSpacing(50)
        
        # === Input Fields ===
        self.user_input = QLineEdit(self.main_frame)
        self.user_input.setPlaceholderText("Username or email")
        self.user_input.setMinimumHeight(55)
        layout.addWidget(self.user_input)
        layout.addSpacing(20)
        
        self.password_input = QLineEdit(self.main_frame)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(55)
        layout.addWidget(self.password_input)
        layout.addSpacing(30)
        
        # === Login Button ===
        self.login_btn = QPushButton("Sign In", self.main_frame)
        self.login_btn.setObjectName("loginButton")
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.login_btn)
        layout.addSpacing(40)
        
        # === Divider ===
        divider = QFrame(self.main_frame)
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("""
            QFrame {
                color: #e2e8f0;
                background: #e2e8f0;
                height: 1px;
                border: none;
            }
        """)
        layout.addWidget(divider)
        layout.addSpacing(30)
        
        # === Registration Section ===
        info_label = QLabel("New to IsraFlight?", self.main_frame)
        info_label.setObjectName("infoLabel")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        layout.addSpacing(8)
        
        self.register_link = QLabel('<a href="#" style="text-decoration: none;">Join our Frequent Flyer Club →</a>', self.main_frame)
        self.register_link.setObjectName("linkLabel")
        self.register_link.setAlignment(Qt.AlignCenter)
        self.register_link.setOpenExternalLinks(False)
        self.register_link.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_link.linkActivated.connect(self.on_register_clicked)
        layout.addWidget(self.register_link)
        
        layout.addStretch()
        
        # Connect login functionality
        self.login_btn.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        self.user_input.returnPressed.connect(self.password_input.setFocus)
    
    def add_animations(self):
        """Add subtle entrance animations"""
        # Initial state - slightly scaled down and transparent
        self.main_frame.setStyleSheet(self.main_frame.styleSheet() + "QFrame#mainFrame { }")
        
        # You could add QPropertyAnimation here for entrance effects
        # This would require more complex implementation with custom properties
    
    def connect_signals(self):
        """Connect authentication signals"""
        self.auth_controller.login_success.connect(self.on_login_success)
        self.auth_controller.login_failure.connect(self.on_login_failure)
    
    def handle_login(self):
        """Handle login with improved UX"""
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password.")
            return
        
        # Update button state with loading indicator
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Signing in...")
        self.login_btn.setStyleSheet(self.login_btn.styleSheet() + """
            QPushButton#loginButton {
                background: #cbd5e0;
                color: #a0aec0;
            }
        """)
        
        self.auth_controller.login(username, password)
    
    def on_login_success(self, user_obj):
        """Handle successful login"""
        self.user_obj = user_obj   # <-- save the user object
        
        if user_obj.Role.lower() == "admin":
            admin_ctrl = AdminController(self.api)
            dlg = AdminWindow(admin_ctrl)
            dlg.setParent(self.parent())  # Set proper parent
            self.accept()  # Close login dialog first
            dlg.show()
        else:
            # Open user dashboard
            self.user_window = UserWindow(user_obj)
            self.user_window.show()
            self.accept()  # Close login dialog

    
    def on_login_failure(self, message):
        """Handle login failure with better UX"""
        self.show_error(f"Login failed: {message}")
        self.reset_login_button()
    
    def show_error(self, message):
        """Show modern error dialog"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Authentication Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""QMessageBox {
            background-color: white;}""")
        
        msg_box.exec()
    
    def reset_login_button(self):
        """Reset login button to original state"""
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In")
        # Remove the disabled styling by resetting to base style
        self.login_btn.setStyleSheet("""
            QPushButton#loginButton {
                font-size: 14pt;
                font-weight: 600;
                color: white;
                border: none;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #1a202c, stop:1 #2d3748);
                padding: 16px 24px;
                min-height: 50px;
            }
            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #2d3748, stop:1 #4a5568);
            }
        """)
    
    def on_register_clicked(self):
        """Handle registration link click"""
        print("🔗 Registration link clicked - opening signup flow...")

        dlg = RegisterDialog(self.api)  
        dlg.exec()  


    
    def paintEvent(self, event):
        """Custom paint event for rounded corners and shadow"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        
        # Fill with semi-transparent background
        painter.fillPath(path, Qt.transparent)
        
        super().paintEvent(event)
        
    def get_user(self):
        """Return logged-in user after dialog closes"""
        return self.user_obj