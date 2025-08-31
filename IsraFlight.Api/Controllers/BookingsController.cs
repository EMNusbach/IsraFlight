using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using IsraFlight.Api.Data;
using IsraFlight.Api.Models;

namespace IsraFlight.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BookingsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public BookingsController(AppDbContext db) { _db = db; }

        // GET: api/bookings
        [HttpGet]
        public IEnumerable<Booking> Get() => _db.Bookings.ToList();

        // GET: api/bookings/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Booking>> GetBooking(int id)
        {
            var booking = await _db.Bookings.FindAsync(id);
            if (booking == null)
            {
                return NotFound();
            }
            return booking;
        }

        // PUT: api/bookings/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutBooking(int id, Booking booking)
        {
            if (id != booking.Id)
            {
                return BadRequest("ID mismatch");
            }

            _db.Entry(booking).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Bookings.Any(b => b.Id == id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/bookings
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] Booking b, [FromServices] HebCalService hebcal)
        {
            var flight = _db.Flights.FirstOrDefault(f => f.Id == b.FlightId);
            if (flight == null)
            {
                Console.WriteLine($"❌ Flight with ID {b.FlightId} not found.");
                return BadRequest($"Flight with ID {b.FlightId} does not exist");
            }

            Console.WriteLine($"✅ Flight found: ID={flight.Id}, Arrival={flight.ArrivalTime}");

            var (isShabbat, parasha, entryTime, exitTime) = await hebcal.GetShabbatInfo(flight.ArrivalTime);

            Console.WriteLine($"🕍 Shabbat Info: IsShabbat={isShabbat}, Parasha={parasha}, Entry={entryTime}, Exit={exitTime}");

            if (isShabbat)
            {
                Console.WriteLine($"⛔ Booking rejected: Flight lands on Shabbat.");
                return BadRequest(new
                {
                    message = "Flight arrival time is on shabbat",
                    parasha,
                    shabbatEntry = entryTime.ToString("HH:mm"),
                    shabbatExit = exitTime.ToString("HH:mm")
                });
            }

            Console.WriteLine("✅ Booking accepted.");
            _db.Bookings.Add(b);
            _db.SaveChanges();
            return Ok(b);
        }



        // DELETE: api/bookings/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBooking(int id)
        {
            var booking = await _db.Bookings.FindAsync(id);
            if (booking == null)
            {
                return NotFound();
            }

            _db.Bookings.Remove(booking);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
