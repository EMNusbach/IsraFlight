namespace Server.Models
{
    public class Airport
    {
        public int Id { get; set; }
        public string Name { get; set; } = "";      
        public string Code { get; set; } = ""; // IATA code (TLV, JFK...)
        public string City { get; set; } = "";  
        public string Country { get; set; } = "";  
    }
}
