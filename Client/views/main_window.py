from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QCursor, QPixmap
from PySide6.QtWidgets import (QLabel, QPushButton, QMainWindow, QGraphicsDropShadowEffect, QWidget)
from controllers.auth_controller import AuthController
from controllers.api_controller import ApiController
from views.login_dialog import LoginDialog
from views.user_window import UserWindow
from views.admin_window import AdminWindow
from controllers.admin_controller import AdminController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IsraFlight - Your Journey Begins Here")
        self.setObjectName("MainWindow")
        self.resize(1200, 800)
        
        # Modern font setup
        font = QFont("Segoe UI", 11)
        font.setWeight(QFont.Medium)
        self.setFont(font)
        self.setMouseTracking(False)
        
        # === Central Widget ===
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        
        # === Background with gradient overlay ===
        self.setup_background()
        
        # === Modern Navbar ===
        self.setup_navbar()
        
        # === Hero Content ===
        self.setup_hero_content()
        
        # === Menu and Status bar (hidden for modern look) ===
        self.menuBar().hide()
        self.statusBar().hide()
        
        # Apply main window styling
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fc, stop:1 #e8f0fe);
            }
        """)
    
    def setup_background(self):
        """Setup background image with modern overlay"""
        self.Img_label = QLabel(self.centralwidget)
        try:
            pixmap = QPixmap("images/main_window_background.png")
            if not pixmap.isNull():
                self.Img_label.setPixmap(pixmap)
            else:
                # Fallback gradient background
                self.Img_label.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #667eea, stop:1 #764ba2);
                    }
                """)
        except:
            # Fallback gradient background
            self.Img_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:1 #764ba2);
                }
            """)
        
        self.Img_label.setScaledContents(True)
        self.Img_label.lower()
        
        # Add overlay for better text contrast
        self.overlay = QLabel(self.centralwidget)
        self.overlay.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 51, 102, 0.3), stop:1 rgba(0, 51, 102, 0.7));
            }
        """)
        self.overlay.lower()
    
    def setup_navbar(self):
        """Setup modern navigation bar"""
        self.navBar = QWidget(self.centralwidget)
        self.navBar.setObjectName("navBar")
        self.navBar.setGeometry(QRect(0, 0, self.width(), 80))
        self.navBar.setStyleSheet("""
            QWidget#navBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                border-bottom: 2px solid #4a5568;
            }
        """)
        self.navBar.setFixedHeight(80)
        
        # Add subtle shadow to navbar
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(Qt.gray)
        shadow.setOffset(0, 2)
        self.navBar.setGraphicsEffect(shadow)
        
        # === Login Button with modern styling ===
        self.Login_Button = QPushButton("Sign In", self.navBar)
        self.Login_Button.setGeometry(QRect(50, 15, 120, 46))
        
        login_font = QFont("Segoe UI", 11)
        login_font.setWeight(QFont.Medium)
        self.Login_Button.setFont(login_font)
        self.Login_Button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.Login_Button.setStyleSheet("""
            QPushButton {
                font-size: 11pt;
                font-weight: 500;
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 22px;
                background: rgba(255, 255, 255, 0.1);
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.05);
            }
        """)
        
        # Add shadow to button
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(10)
        btn_shadow.setColor(Qt.darkGray)
        btn_shadow.setOffset(0, 3)
        self.Login_Button.setGraphicsEffect(btn_shadow)
        
        self.Login_Button.clicked.connect(self.open_login_dialog)
        
        # === Brand Logo/Title ===
        self.h1_label = QLabel("IsraFlight", self.navBar)
        self.h1_label.setGeometry(QRect(self.width() - 180, 25, 150, 35))
        
        brand_font = QFont("Segoe UI", 18)
        brand_font.setWeight(QFont.Bold)
        self.h1_label.setFont(brand_font)
        self.h1_label.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: white;
                background-color: transparent;
                letter-spacing: 1px;
            }
        """)
    
    def setup_hero_content(self):
        """Setup hero section with modern typography"""
        # === Main Heading ===
        self.h2_label = QLabel("Discover Your Next\nAdventure", self.centralwidget)
        self.h2_label.setGeometry(QRect(60, 200, 800, 150))
        
        hero_font = QFont("Segoe UI", 42)
        hero_font.setWeight(QFont.Bold)
        self.h2_label.setFont(hero_font)
        self.h2_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: transparent;
                font-size: 42pt;
                font-weight: bold;
                line-height: 1.2;
            }
        """)
        self.h2_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    
    def resizeEvent(self, event):
        """Handle window resize with modern responsive behavior"""
        # === Resize navbar ===
        self.navBar.setGeometry(QRect(0, 0, self.width(), 80))
        
        # === Reposition brand label ===
        self.h1_label.setGeometry(QRect(self.width() - 180, 25, 150, 35))
        
        # === Resize background and overlay ===
        nav_height = self.navBar.height()
        bg_rect = QRect(0, nav_height, self.width(), self.height() - nav_height)
        self.Img_label.setGeometry(bg_rect)
        self.overlay.setGeometry(bg_rect)
        
        super().resizeEvent(event)
    
    def open_login_dialog(self):
        api = ApiController(base_url="http://localhost:5126/api")
        auth_controller = AuthController(api=api)
        dialog = LoginDialog(auth_controller, api)
        # dialog.setParent(self)

        if dialog.exec():
            user = dialog.get_user()
            print("✅ Login successful!", user)

            if user.Role.lower() == "admin":
                self.admin_window = AdminWindow(AdminController(api))
                self.admin_window.show()
            else:
                self.user_window = UserWindow(user)
                self.user_window.show()


            self.close()  # close landing page
        else:
            print("❌ Login cancelled.")
