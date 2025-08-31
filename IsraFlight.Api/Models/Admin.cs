namespace IsraFlight.Api.Models
{
    public class Admin
    {
        public int Id { get; set; }
        public string Username { get; set; } = "";
        public string PasswordHash { get; set; } = "";   
        public string Email { get; set; } = "";
    }
}
