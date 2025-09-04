# utils/pdf_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import os

def generate_ticket_pdf(booking, flight, filename=None):
    if filename is None:
        filename = f"ticket_{booking.id or 'unknown'}.pdf"
        
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 80

    c.setFont("Helvetica-Bold", 18)
    c.drawString(80, y, "IsraFlight — Boarding Pass")
    c.setFont("Helvetica", 12)
    y -= 40
    c.drawString(80, y, f"Booking ID: {booking.id}")
    y -= 20
    c.drawString(80, y, f"User ID: {booking.frequentFlyerId}")
    y -= 20
    c.drawString(80, y, f"Flight ID: {booking.flightId}")
    y -= 20
    c.drawString(80, y, f"Seat: {booking.seat or 'N/A'}")
    y -= 20
    c.drawString(80, y, f"Departure: {flight.DepartureLocation}")
    y -= 20
    c.drawString(80, y, f"Landing: {flight.LandingLocation}")
    y -= 40
    c.drawString(80, y, f"Issued: {datetime.datetime.now().isoformat()}")

    c.showPage()
    c.save()
    return os.path.abspath(filename)
