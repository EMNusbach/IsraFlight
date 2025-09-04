using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;

namespace Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class BookingsController : ControllerBase
    {
        private readonly AppDbContext _db;
        private readonly HebCalService _hebcal;


        public BookingsController(AppDbContext db, HebCalService hebcal) 
        { 
            _db = db; 
            _hebcal = hebcal;
        }

        // GET: api/bookings
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Booking>>> Get()
        {
            try
            {
                return Ok(await _db.Bookings.ToListAsync());
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Error retrieving bookings");
            }
        }

        // GET: api/bookings/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Booking>> GetBooking(int id)
        {
            try
            {
                var booking = await _db.Bookings.FindAsync(id);
                if (booking == null)
                {
                    return NotFound();
                }
                return Ok(booking);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Error retrieving booking");
            }
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
                if (!await _db.Bookings.AnyAsync(b => b.Id == id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Error updating booking");
            }

            return NoContent();
        }

        // POST: api/bookings
        [HttpPost]
        public async Task<IActionResult> Post([FromBody] Booking b)
        {
            try
            {
                // Validate the booking object
                if (b == null)
                {
                    return BadRequest("Booking data is required");
                }

                // Check if flight exists
                var flight = await _db.Flights.FirstOrDefaultAsync(f => f.Id == b.FlightId);
                if (flight == null)
                {
                    return BadRequest($"Flight with ID {b.FlightId} does not exist");
                }

                // Check Shabbat info
                var (isShabbat, parasha, entryTime, exitTime) = await _hebcal.GetShabbatInfo(flight.ArrivalTime);
                if (isShabbat)
                {
                    return BadRequest(new
                    {
                        message = "Flight arrival time is on shabbat",
                        parasha,
                        shabbatEntry = entryTime.ToString("HH:mm"),
                        shabbatExit = exitTime.ToString("HH:mm")
                    });
                }

                // Set any required fields that might be missing
                // You may need to adjust these based on your Booking model
                if (b.BookingDate == default(DateTime))
                {
                    b.BookingDate = DateTime.Now;
                }

                _db.Bookings.Add(b);
                await _db.SaveChangesAsync();

                return CreatedAtAction(nameof(GetBooking), new { id = b.Id }, b);
            }
            catch (DbUpdateException dbEx)
            {
                
                // More specific error handling
                if (dbEx.InnerException?.Message.Contains("FOREIGN KEY") == true)
                {
                    return BadRequest("Invalid foreign key reference. Please check FlightId and other referenced IDs.");
                }
                if (dbEx.InnerException?.Message.Contains("UNIQUE") == true)
                {
                    return BadRequest("A booking with these details already exists.");
                }
                if (dbEx.InnerException?.Message.Contains("NOT NULL") == true)
                {
                    return BadRequest("Required fields are missing. Please check all required booking information.");
                }
                
                return StatusCode(500, $"Database error: {dbEx.InnerException?.Message ?? dbEx.Message}");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error creating booking: {ex.Message}");
            }
        }

        // DELETE: api/bookings/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBooking(int id)
        {
            try
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
            catch (Exception ex)
            {
                return StatusCode(500, "Error deleting booking");
            }
        }
    }
}