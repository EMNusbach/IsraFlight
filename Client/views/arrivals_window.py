from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QHBoxLayout, QFrame, QGraphicsDropShadowEffect, QHeaderView,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QFont


class ArrivalsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IsraFlight - TLV Arrivals")
        self.setFixedSize(1200, 700)  # Slightly larger for better readability
        
        # Set window icon if you have one
        # self.setWindowIcon(QIcon("path/to/icon.png"))

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        header_label = QLabel("Ben Gurion Airport - Real-time Arrivals")
        header_label.setObjectName("welcomeLabel")
        header_label.setAlignment(Qt.AlignCenter)
        
        # Make header more prominent
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        header_label.setFont(font)
        
        self.layout.addWidget(header_label)

        # Controls: Hours Ahead + Refresh
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(10, 10, 10, 10)

        # Hours selection
        hours_label = QLabel("Hours ahead:")
        hours_label.setMinimumWidth(80)
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 5)  # Match backend validation
        self.hours_spin.setValue(3)  # More reasonable default
        self.hours_spin.setMinimumWidth(60)
        self.hours_spin.setToolTip("Select how many hours ahead to show arrivals (1-5 hours)")
        
        controls_layout.addWidget(hours_label)
        controls_layout.addWidget(self.hours_spin)
        
        # Add spacer
        controls_layout.addStretch()

        # Refresh button
        self.refresh_btn = QPushButton("🔄 Load Arrivals")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.setMinimumHeight(35)
        self.refresh_btn.setMinimumWidth(150)
        self.refresh_btn.setToolTip("Click to refresh arrival data")
        controls_layout.addWidget(self.refresh_btn)

        self.layout.addWidget(controls_frame)

        # Status label for feedback
        self.status_label = QLabel("Click 'Load Arrivals' to fetch current data")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        self.layout.addWidget(self.status_label)

        # Table
        self.table = QTableWidget()
        self.setup_table()
        self.layout.addWidget(self.table)

        # Apply styling
        self.apply_styles()

        # Shadow for frame (match your other windows)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 10)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

    def setup_table(self):
        """Configure the arrivals table"""
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Flight", "Airline", "From", "Scheduled Arrival", "Terminal", "Status"
        ])

        header = self.table.horizontalHeader()
        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col, 190)  # same width for all columns

        # Table behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(35)


    def apply_styles(self):
        """Apply custom styles to the window"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #welcomeLabel {
                color: #2c3e50;
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #3498db;
            }
            
            #controlsFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            
            #statusLabel {
                padding: 5px;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #21618c;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            
            QSpinBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            
            QTableWidget {
                background-color: white;
                gridline-color: #e1e8ed;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e1e8ed;
            }
            
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            
            QHeaderView::section:last {
                border-top-right-radius: 8px;
            }
        """)

    def update_status(self, message, is_error=False):
        """Update the status label"""
        if is_error:
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #27ae60; font-style: italic;")
        self.status_label.setText(message)

    def set_loading_state(self, loading=True):
        """Enable/disable controls during loading"""
        self.refresh_btn.setEnabled(not loading)
        self.hours_spin.setEnabled(not loading)
        
        if loading:
            self.refresh_btn.setText("🔄 Loading...")
            self.update_status("Loading arrivals data...")
        else:
            self.refresh_btn.setText("🔄 Load Arrivals")