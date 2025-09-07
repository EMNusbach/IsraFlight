from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QTableWidgetItem
from datetime import datetime
from .api_controller import ApiController
from views.arrivals_window import ArrivalsWindow


class ArrivalsController(QObject):
    # Signals for UI updates
    data_loaded = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, window: ArrivalsWindow, api: ApiController):
        super().__init__()
        self.window = window
        self.api = api

        # Connect refresh button
        self.window.refresh_btn.clicked.connect(self.load_arrivals)

    def load_arrivals(self):
        """Fetch arrivals from API and update table."""
        hours = self.window.hours_spin.value()
        try:
            flights = self.api.get(f"/flights/arrivals?hoursAhead={hours}")

            if isinstance(flights, dict):
                flights = flights.get("data", [])

            print(f"Fetched {len(flights)} arrivals")
            self.populate_table(flights)
            self.data_loaded.emit(flights)

        except Exception as e:
            self.window.table.setRowCount(1)
            self.window.table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            self.error_occurred.emit(str(e))

    def populate_table(self, flights: list):
        """Fill the arrivals QTableWidget with data."""
        table = self.window.table
        table.setRowCount(0)

        if not flights:
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem("No arrivals found"))
            return

        for flight in flights:
            row = table.rowCount()
            table.insertRow(row)

            flight_number = flight.get("flightNumber", flight.get("flight_number", ""))
            airline = flight.get("airline", flight.get("Airline", ""))
            origin = flight.get("origin", flight.get("Origin", ""))
            terminal = flight.get("terminal", flight.get("Terminal", ""))
            gate = flight.get("gate", flight.get("Gate", ""))
            status = flight.get("status", flight.get("Status", ""))
            sched = flight.get("scheduledArrival", flight.get("scheduled_arrival", ""))

            # Format time
            try:
                dt = sched if isinstance(sched, datetime) else datetime.fromisoformat(sched)
                sched_str = dt.strftime("%b %d, %H:%M")
            except:
                sched_str = str(sched)

            values = [flight_number, airline, origin, sched_str, terminal, gate, status]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))

                # ✅ Status coloring
                if col == 6:  # status column
                    status_lower = str(val).lower()
                    if "active" in status_lower:
                        item.setForeground(self.window.green_brush)
                    elif "delay" in status_lower:
                        item.setForeground(self.window.red_brush)
                    else:
                        item.setForeground(self.window.gray_brush)

                table.setItem(row, col, item)
