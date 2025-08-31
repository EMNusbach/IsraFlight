namespace IsraFlight.Api.Models
{
    public class Booking
    {
        public int Id { get; set; }

        public int PassengerId { get; set; }

        public int FlightId { get; set; }

        public DateTime BookingDate { get; set; }

        // All tickets in this booking
        public List<Ticket> Tickets { get; set; } = new List<Ticket>();
        
    }
}
