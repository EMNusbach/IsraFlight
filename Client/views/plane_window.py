from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QGridLayout, QFrame, QHBoxLayout, QMessageBox, QLineEdit, QMainWindow)
from PySide6.QtGui import QPixmap, QFont, QCursor
from PySide6.QtCore import Qt
import requests
from io import BytesIO

from models import Plane  
from dataclasses import asdict


class PlaneWindow(QMainWindow):
    def __init__(self, plane_controller, parent=None):
        super().__init__(parent)
        self.controller = plane_controller
        self.editing_cards = set()  # Track which cards are in edit mode

        self.setWindowTitle("plane Management")
        self.resize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # === Main layout ===
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Navigation Bar ===
        nav_bar = QWidget()
        nav_bar.setObjectName("navBar")
        nav_bar.setFixedHeight(80)

        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(30, 20, 30, 20)

        # Back Button
        self.btn_back = QPushButton("←")
        self.btn_back.setObjectName("backButton")
        self.btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_back.clicked.connect(self.close)

        # Title (centered)
        lbl_title = QLabel("✈ Available Planes")
        lbl_title.setObjectName("titleLabel")
        lbl_title.setAlignment(Qt.AlignCenter)

        # Brand (with proper spacing)
        lbl_brand = QLabel("IsraFlight")
        lbl_brand.setObjectName("brandLabel")
        lbl_brand.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch(1)  # Push title to center
        nav_layout.addWidget(lbl_title)
        nav_layout.addStretch(1)  # Balance the layout
        nav_layout.addWidget(lbl_brand)

        main_layout.addWidget(nav_bar)

        # === Content Area ===
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget") 
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Add Plane Button (top-left of content)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 10)

        self.btn_add = QPushButton("➕ Add New Plane")
        self.btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_add.setObjectName("addButton")
        self.btn_add.clicked.connect(self.add_plane)
        self.btn_add.setStyleSheet("QPushButton#addButton {color: white;}")
        button_layout.addWidget(self.btn_add)
        button_layout.addStretch()

        content_layout.addWidget(button_container)

        # === Scroll Area ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        content_layout.addWidget(scroll)

        # === Container for cards ===
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(container)

        main_layout.addWidget(content_widget)

        # === Custom styles ===
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }

            QWidget#contentWidget {
                background-color: #f5f7fa;
            }             
            
            QWidget#navBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                border-bottom: 2px solid #4a5568;
                border-radius: 0px;
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
                min-width: 120px;
            }
            
            QPushButton#addButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                border: none;
            }
            
            QPushButton#addButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
            
            QPushButton.navButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a202c, stop:1 #2d3748);
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }
            
            QPushButton.navButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #4a5568);
            }
            
            QPushButton.deleteButton {
                background: #dc3545;
                color: white;
                padding: 6px 12px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }
            
            QPushButton.deleteButton:hover {
                background: #c82333;
            }
            
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
            
            QLineEdit:focus {
                border-color: #1a202c;
            }
        """)

        self.load_planes()

    def load_planes(self):
        """Load all planes from controller and display them"""
        # Clear old items
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        planes = self.controller.get_all_planes()

        if not planes:
            QMessageBox.warning(self, "Error", "No planes found or API error.")
            return

        row, col = 0, 0
        for plane in planes:
            try:
                # Normalize field names to lowercase for consistency
                normalized_plane = self.normalize_plane_data(plane)
                card = self.create_plane_card(normalized_plane)
                self.grid.addWidget(card, row, col)
                col += 1
                if col == 3:  # 3 cards per row
                    col = 0
                    row += 1
            except Exception as e:
                print(f"Failed to load plane card: {e}")

    def normalize_plane_data(self, plane):
        """Normalize plane data field names to consistent lowercase format"""
        normalized = {}
        
        # Handle different field name formats
        field_mapping = {
            'id': ['id', 'Id', 'ID'],
            'manufacturer': ['manufacturer', 'Manufacturer', 'Manufacturr'],  # Note: fixed typo
            'nickname': ['nickname', 'Nickname', 'Nick'],
            'year': ['year', 'Year'],
            'imageUrl': ['imageUrl', 'ImageUrl', 'image_url', 'Image_Url']
        }
        
        for standard_key, possible_keys in field_mapping.items():
            for key in possible_keys:
                if key in plane:
                    normalized[standard_key] = plane[key]
                    break
            else:
                # Default value if key not found
                if standard_key == 'year':
                    normalized[standard_key] = 0
                elif standard_key == 'id':
                    normalized[standard_key] = None
                else:
                    normalized[standard_key] = ''
        
        return normalized

    def create_plane_card(self, plane):
        """Create a plane card widget"""
        card = QFrame()
        card.setFixedSize(300, 380)
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
            QFrame:hover {
                border: 1px solid #cbd5e0;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Store plane data and state
        card.plane_data = plane.copy()
        card.is_new = plane.get('id') is None

        # === Plane Image ===
        img_label = QLabel()
        img_label.setFixedHeight(140)
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setStyleSheet("border: none;")
        card.img_label = img_label

        self.load_image(img_label, plane.get("imageUrl"))
        layout.addWidget(img_label)

        # === Manufacturer (under image) ===
        manufacturer_label = QLabel(plane.get('manufacturer', 'Unknown'))
        manufacturer_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        manufacturer_label.setAlignment(Qt.AlignCenter)
        manufacturer_label.setStyleSheet("color: #2d3748; margin-bottom: 5px; border: none;")
        layout.addWidget(manufacturer_label)
        card.manufacturer_label = manufacturer_label

        # === Info Fields Container ===
        info_widget = QWidget()
        card.info_widget = info_widget
        layout.addWidget(info_widget)

        # Create display mode initially
        self.create_display_mode(card)

        # === Buttons ===
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        edit_btn = QPushButton("Edit" if not card.is_new else "Save")
        edit_btn.setProperty("class", "navButton")
        edit_btn.clicked.connect(lambda: self.handle_edit_save(card))

        delete_btn = QPushButton("Delete")
        delete_btn.setProperty("class", "deleteButton")
        delete_btn.clicked.connect(lambda: self.delete_plane(plane["id"]))

        button_layout.addWidget(edit_btn)
        if not card.is_new:  # Don't show delete for new planes
            button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)

        card.edit_btn = edit_btn
        card.delete_btn = delete_btn

        # If it's a new plane, start in edit mode
        if card.is_new:
            self.create_edit_mode(card)

        return card

    def create_field_layout(self, label_text, value, is_edit_mode=False, field_name=None, card=None):
        """Helper function to create consistent field layouts"""
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)

        # Label
        label = QLabel(f"{label_text}:")
        label.setStyleSheet("font-weight: bold; border: none; color: #2d3748;")
        layout.addWidget(label)

        if is_edit_mode and field_name != 'id':  # ID is always read-only
            # Editable field
            edit_field = QLineEdit(str(value))
            layout.addWidget(edit_field)
            
            # Special handling for image URL to update preview
            if field_name == 'imageUrl':
                edit_field.textChanged.connect(lambda text: self.update_image_preview(card, text))
            
            return layout, edit_field
        else:
            # Display field
            value_label = QLabel(str(value) if value is not None else '-')
            value_label.setStyleSheet("color: #4a5568; border: none;")
            layout.addWidget(value_label)
            layout.addStretch()
            return layout, value_label
        

    def create_display_mode(self, card):
        """Create the display mode layout for a card"""
        layout = card.info_widget.layout()

        # Clear existing layout
        if not layout:
            layout = QVBoxLayout(card.info_widget)
        card.info_layout = layout
        self.clear_layout(layout)

        card.info_layout.setSpacing(5)
        card.info_layout.setContentsMargins(0, 0, 0, 0)

        plane = card.plane_data

        # Create fields
        id_layout, card.id_display = self.create_field_layout("ID", plane.get('id'), False)
        card.info_layout.addLayout(id_layout)

        nickname_layout, card.nickname_display = self.create_field_layout("Nickname", plane.get('nickname'), False)
        card.info_layout.addLayout(nickname_layout)

        year_layout, card.year_display = self.create_field_layout("Year", plane.get('year'), False)
        card.info_layout.addLayout(year_layout)

    def create_edit_mode(self, card):
        """Create the edit mode layout for a card"""
        layout = card.info_widget.layout()
                
        # Clear existing layout
        if not layout:
            layout = QVBoxLayout(card.info_widget)
        card.info_layout = layout
        self.clear_layout(layout)

        card.info_layout.setSpacing(5)
        card.info_layout.setContentsMargins(0, 0, 0, 0)

        plane = card.plane_data

        # Create editable fields
        if not card.is_new:
            # Show ID for existing planes (read-only)
            id_layout, _ = self.create_field_layout("ID", plane.get('id'), False)
            card.info_layout.addLayout(id_layout)

        # Image URL
        img_url_layout, card.img_url_edit = self.create_field_layout(
            "Image URL", plane.get('imageUrl'), True, 'imageUrl', card
        )
        card.info_layout.addLayout(img_url_layout)

        # Manufacturer
        manufacturer_layout, card.manufacturer_edit = self.create_field_layout(
            "Manufacturer", plane.get('manufacturer'), True, 'manufacturer', card
        )
        card.info_layout.addLayout(manufacturer_layout)

        # Nickname
        nickname_layout, card.nickname_edit = self.create_field_layout(
            "Nickname", plane.get('nickname'), True, 'nickname', card
        )
        card.info_layout.addLayout(nickname_layout)

        # Year
        year_layout, card.year_edit = self.create_field_layout(
            "Year", plane.get('year'), True, 'year', card
        )
        card.info_layout.addLayout(year_layout)

    def clear_layout(self, layout):
        """Helper function to clear all widgets from a layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget:
                widget.setParent(None)
                widget.deleteLater()
            elif child_layout:
                self.clear_layout(child_layout)
                child_layout.setParent(None)
                child_layout.deleteLater()

    def handle_edit_save(self, card):
        """Handle edit/save button click"""
        plane_id = card.plane_data.get('id')
        
        if card.is_new:
            # Save new plane
            self.save_new_plane(card)
        elif plane_id in self.editing_cards:
            # Save existing plane changes
            self.save_plane_changes(card)
        else:
            # Enter edit mode
            self.enter_edit_mode(card)

    def enter_edit_mode(self, card):
        """Switch card to edit mode"""
        plane_id = card.plane_data['id']
        self.editing_cards.add(plane_id)
        
        # Change button text
        card.edit_btn.setText("Save")
        
        # Create edit layout
        self.create_edit_mode(card)

    def update_image_preview(self, card, url):
        """Update image preview when URL changes"""
        if url.strip():
            self.load_image(card.img_label, url.strip())
        else:
            card.img_label.setText("No Image")
            card.img_label.setStyleSheet("color: #666; font-style: italic;")

    def save_plane_changes(self, card):
        """Save changes to an existing plane"""
        plane_id = card.plane_data['id']
        
        try:
            # Get updated values
            updated_data = {
                'id': plane_id,
                'manufacturer': card.manufacturer_edit.text().strip(),
                'nickname': card.nickname_edit.text().strip(),
                'year': int(card.year_edit.text()) if card.year_edit.text().isdigit() else 0,
                'imageUrl': card.img_url_edit.text().strip()
            }
            
            # Update via controller
            result = self.controller.update_plane(plane_id, updated_data)
            
            if result["success"]:
                # Update card data
                card.plane_data.update(updated_data)
                
                # Exit edit mode
                self.editing_cards.remove(plane_id)
                card.edit_btn.setText("Edit")
                
                # Update manufacturer display
                card.manufacturer_label.setText(updated_data['manufacturer'] or 'Unknown')
                
                # Switch back to display mode
                self.create_display_mode(card)
                
                QMessageBox.information(self, "Success", "Plane updated successfully!")
            else:
                QMessageBox.warning(self, "Error",f"Failed to update plane: {result["error"]}")
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid year.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error saving changes: {str(e)}")

    def save_new_plane(self, card):
        """Save a new plane"""
        try:
            # Validate required fields
            manufacturer = card.manufacturer_edit.text().strip()
            if not manufacturer:
                QMessageBox.warning(self, "Error", "Manufacturer is required.")
                return

            # Create new plane data
            new_plane_data = {
                'manufacturer': manufacturer,
                'nickname': card.nickname_edit.text().strip(),
                'year': int(card.year_edit.text()) if card.year_edit.text().isdigit() else 0,
                'imageUrl': card.img_url_edit.text().strip()
            }
            
            # Add via controller
            result = self.controller.add_plane(new_plane_data)
            
            if result["success"]:
                QMessageBox.information(self, "Success", "Plane added successfully!")
                self.load_planes()  # Reload all planes
            else:
                QMessageBox.warning(self, "Error",f"Failed to add plane: {result["error"]}")
                
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid year.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error adding plane: {str(e)}")

    def add_plane(self):
        """Add a new plane card at the top"""
        # Create new plane data
        new_plane_data = {
            'id': None,  # Will be assigned by API
            'manufacturer': '',
            'nickname': '',
            'year': 0,
            'imageUrl': ''
        }

        card = self.create_plane_card(new_plane_data)

        # Shift existing cards down
        self.shift_cards_down()
        
        # Add new card at top-left
        self.grid.addWidget(card, 0, 0)

    def shift_cards_down(self):
        """Helper function to shift all existing cards down by one row"""
        items = []
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i)
            widget = item.widget()
            if widget:
                row, col, rowspan, colspan = self.grid.getItemPosition(i)
                items.append((widget, row, col, rowspan, colspan))

        # Remove all widgets
        for widget, _, _, _, _ in items:
            self.grid.removeWidget(widget)

        # Re-add with incremented row
        for widget, row, col, rowspan, colspan in items:
            self.grid.addWidget(widget, row + 1, col, rowspan, colspan)

    def load_image(self, img_label, image_url):
        """Load and display an image from URL"""
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data.read())
                    img_label.setPixmap(pixmap.scaled(270, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    img_label.setText("Image failed to load")
                    img_label.setStyleSheet("color: #666; font-style: italic;")
            except Exception as e:
                img_label.setText("Image error")
                img_label.setStyleSheet("color: #666; font-style: italic;")
        else:
            img_label.setText("No Image")
            img_label.setStyleSheet("color: #666; font-style: italic;")

    def delete_plane(self, plane_id):
        """Delete a plane"""
        confirm = QMessageBox.question(
            self, 
            "Delete Plane", 
            "Are you sure you want to delete this plane?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            success = self.controller.delete_plane(plane_id)
            if success:
                QMessageBox.information(self, "Deleted", "Plane deleted successfully.")
                self.load_planes()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete plane.")