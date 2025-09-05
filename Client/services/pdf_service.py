from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.graphics.barcode import code128
from reportlab.lib.units import cm, mm
import datetime, os
import qrcode
from reportlab.lib.utils import ImageReader


def generate_qr_code(data, path="qr_temp.png"):
    img = qrcode.make(data)
    img.save(path)
    return path


def generate_ticket_pdf(booking, flight, traveler_name, dep_airport_name, arr_airport_name):
    """
    Generates a boarding pass PDF for a booking.
    traveler_name, dep_airport_name, arr_airport_name are required.
    """
    filename = f"PDF_files/ticket_{traveler_name.replace(' ', '_')}_{booking.id}.pdf"
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # === Header ===
    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(70, height - 70, "IsraFlight ✈ Boarding Pass")
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.line(50, height - 80, width - 50, height - 80)

    # === Passenger Info ===
    y = height - 140
    c.setFillColor(colors.lightgrey)
    c.roundRect(50, y-60, width-100, 70, 10, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, y-20, f"Passenger: {traveler_name}")
    c.setFont("Helvetica", 14)
    c.drawString(70, y-45, f"Booking ID: {booking.id}")
    c.drawString(300, y-45, f"User ID: {booking.frequentFlyerId}")

    # === Flight Info ===
    y -= 120
    c.setFillColor(colors.whitesmoke)
    c.roundRect(50, y-100, width-100, 110, 10, fill=True, stroke=True)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(70, y-20, f"From: {dep_airport_name} ({flight.departureAirportId})")
    c.drawString(70, y-50, f"To:   {arr_airport_name} ({flight.arrivalAirportId})")
    c.setFont("Helvetica", 14)
    c.drawString(70, y-80, f"Departure: {flight.departureTime}")
    c.drawString(350, y-80, f"Arrival: {flight.arrivalTime}")

    # === Barcode and QR ===
    y = 160
    barcode_value = f"{booking.id}-{flight.id}-{booking.frequentFlyerId}"
    barcode = code128.Code128(barcode_value, barHeight=25*mm, barWidth=1.0)
    barcode.drawOn(c, 60, y)
    qr_data = f"Booking:{booking.id}, Flight:{flight.id}, User:{booking.frequentFlyerId}"
    qr_path = generate_qr_code(qr_data)
    qr_img = ImageReader(qr_path)
    c.drawImage(qr_img, width-180, y-10, width=100, height=100)

    # === Footer ===
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawString(60, 60, f"Issued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.showPage()
    c.save()
    return os.path.abspath(filename)
