from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QTableWidget, QHeaderView, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QColor, QBrush


class ArrivalsWindow(QMainWindow):
    def __init__(self, api_controller, parent=None):
        super().__init__(parent)
        self.api = api_controller
        self.setWindowTitle("IsraFlight - TLV Arrivals")
        self.setMinimumSize(1200, 700)

        # Color brushes for status highlighting
        self.green_brush = QBrush(QColor("#19D619"))
        self.red_brush = QBrush(QColor("#e74c3c"))
        self.gray_brush = QBrush(QColor("#718096"))

        # === Central layout ===
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Nav Bar ===
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(80)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 20, 30, 20)

        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")   # 👈 important
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.clicked.connect(self.close)


        title_label = QLabel("✈ Arrivals - Ben Gurion Airport")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)

        brand_label = QLabel("IsraFlight")
        brand_label.setObjectName("brandLabel")
        brand_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch(1)
        nav_layout.addWidget(title_label)
        nav_layout.addStretch(1)
        nav_layout.addWidget(brand_label)
        main_layout.addWidget(nav_bar)

        # === Controls ===
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(40, 20, 40, 10)

        hours_label = QLabel("Hours ahead:")
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 5)
        self.hours_spin.setValue(3)

        self.refresh_btn = QPushButton("🔄 Load Arrivals")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))

        controls_layout.addWidget(hours_label)
        controls_layout.addWidget(self.hours_spin)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_btn)
        main_layout.addWidget(controls_frame)

        # === Status Label ===
        self.status_label = QLabel("Click 'Load Arrivals' to fetch current data")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #718096; font-style: italic;")
        main_layout.addWidget(self.status_label)

        # === Arrivals Table ===
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Flight", "Airline", "Origin", "Arrival Time", "Terminal", "Gate", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                font-size: 12pt;
            }
            QHeaderView::section {
                background-color: #2d3748;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
        """)
        main_layout.addWidget(self.table)

        self.setStyleSheet(self.get_styles())

    def get_styles(self):
        return """
        QMainWindow { background-color: #f8fafc; }
        QWidget#navBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #1a202c, stop:1 #2d3748);
            border-bottom: 2px solid #4a5568;
        }
        QLabel#titleLabel { font-size: 20pt; font-weight: bold; color: white; }
        QLabel#brandLabel { font-weight: bold; color: white; font-size: 16pt; }
        QPushButton { font-weight: bold; border-radius: 6px; padding: 6px 12px; }
        QPushButton:hover { opacity: 0.85; }
        
        QPushButton#backButton {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
        font-size: 16pt;
        font-weight: bold;
        padding: 6px 12px;
        min-width: 35px;
        min-height: 25px;
        }
        QPushButton#backButton:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        """
