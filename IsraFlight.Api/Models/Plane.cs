namespace IsraFlight.Api.Models
{
    public class Plane
    {
        public int Id { get; set; }
        public string Manufacturer { get; set; } = "";
        public string Nickname { get; set; } = "";
        public int Year { get; set; }
        public string ImageUrl { get; set; } = "";
    }
}
