from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem
from .api_controller import ApiController
from views.arrivals_window import ArrivalsWindow
from datetime import datetime

class ArrivalsController(QObject):
    # Signals for UI updates
    data_loaded = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, window: ArrivalsWindow, api: ApiController):
        super().__init__()
        self.window = window
        self.api = api

        # Connect the Load Arrivals button
        self.window.refresh_btn.clicked.connect(self.load_arrivals)

    def load_arrivals(self):
        hours = self.window.hours_spin.value()
        try:
            # Call your backend
            flights = self.api.get(f"/flights/arrivals?hoursAhead={hours}")

            # Handle wrapper and default to empty list
            if isinstance(flights, dict):
                flights = flights.get("data", [])
            
            print(f"Fetched {len(flights)} arrivals")
            print(f"Sample data: {flights[:2]}")  # Print first 2 entries for inspection

            self.populate_table(flights)
            self.data_loaded.emit(flights)

        except Exception as e:
            self.window.table.setRowCount(1)
            self.window.table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            self.error_occurred.emit(str(e))


    def populate_table(self, flights):
        self.window.table.setRowCount(len(flights))

        for row, flight in enumerate(flights):
            # Keys handling
            flight_number = flight.get("flightNumber") or flight.get("flight_number") or ""
            airline = flight.get("Airline") or flight.get("airline") or ""
            origin = flight.get("Origin") or flight.get("origin") or ""
            terminal = flight.get("Terminal") or flight.get("terminal") or ""
            status = flight.get("Status") or flight.get("status") or ""

            # Scheduled arrival
            sched = flight.get("scheduledArrival") or flight.get("scheduled_arrival") or ""
            scheduled_arrival_str = ""
            if sched:
                try:
                    dt = sched if isinstance(sched, datetime) else datetime.fromisoformat(sched)
                    scheduled_arrival_str = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    scheduled_arrival_str = str(sched)

            # Populate cells
            self.window.table.setItem(row, 0, QTableWidgetItem(flight_number))
            self.window.table.setItem(row, 1, QTableWidgetItem(airline))
            self.window.table.setItem(row, 2, QTableWidgetItem(origin))
            self.window.table.setItem(row, 3, QTableWidgetItem(scheduled_arrival_str))
            self.window.table.setItem(row, 4, QTableWidgetItem(terminal))
            self.window.table.setItem(row, 5, QTableWidgetItem(status))

            # Highlight active flights
           # Highlight active and delayed flights
            if status.lower() == "active":
                status_item = self.window.table.item(row, 5)  # Status column
                if status_item:
                    status_item.setForeground(QColor("#19D619"))  # green text
            elif status.lower() == "delayed":
                # Only change the text color of the Status cell
                status_item = self.window.table.item(row, 5)  # Status column
                if status_item:
                    status_item.setForeground(QColor("#e74c3c"))  # red text
