using Microsoft.EntityFrameworkCore;
using Server.Models;

namespace Server.Data
{
    /// The Entity Framework Core database context for the IsraFlight API.
    /// Manages access to the database and maps models to database tables.
    public class AppDbContext : DbContext
    {
        /// Constructor that accepts options to configure the DbContext, such as the connection string.
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        /// Represents the Tables in the database.
        public DbSet<Plane> Planes => Set<Plane>();
        public DbSet<Airport> Airports => Set<Airport>();
        public DbSet<Flight> Flights => Set<Flight>();
        public DbSet<FrequentFlyer> FrequentFlyers => Set<FrequentFlyer>();
        public DbSet<Booking> Bookings => Set<Booking>();
        public DbSet<Ticket> Tickets => Set<Ticket>();
        public DbSet<Admin> Admins => Set<Admin>();
        public DbSet<Auth> Auths => Set<Auth>();


    }
}
