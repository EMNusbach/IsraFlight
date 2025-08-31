namespace IsraFlight.Api.Models
{
    public class Ticket
    {
        public int Id { get; set; }

        public int BookingId { get; set; }

        public int FlightId { get; set; }

        public string Seat { get; set; } = "";

        public decimal Price{get; set;}

        public string PdfUrl { get; set; } = "";      // URL for PDF

    }
}
