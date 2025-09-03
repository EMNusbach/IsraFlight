using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;

namespace Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FlightsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public FlightsController(AppDbContext db) { _db = db; }

        // GET: api/flights
        [HttpGet]
        public IEnumerable<Flight> Get() => _db.Flights.ToList();

        // GET: api/flights/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Flight>> GetFlight(int id)
        {
            var flight = await _db.Flights.FindAsync(id);
            if (flight == null)
            {
                return NotFound();
            }
            return flight;
        }

        // PUT: api/flights/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFlight(int id, [FromBody] Flight flight)
        {
            if (id != flight.Id)
            {
                return BadRequest("ID mismatch");
            }

            _db.Entry(flight).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Flights.Any(f => f.Id == id))
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

        // POST: api/flights
        [HttpPost]
        public IActionResult Post(Flight f)
        {
            // Validate Plane exists
            var planeExists = _db.Planes.Any(p => p.Id == f.PlaneId);
            if (!planeExists)
                return BadRequest($"Plane with ID {f.PlaneId} does not exist.");

            // Validate Departure Airport
            var departureExists = _db.Airports.Any(a => a.Id == f.DepartureAirportId);
            if (!departureExists)
                return BadRequest($"Departure airport with ID {f.DepartureAirportId} does not exist.");

            // Validate Arrival Airport
            var arrivalExists = _db.Airports.Any(a => a.Id == f.ArrivalAirportId);
            if (!arrivalExists)
                return BadRequest($"Arrival airport with ID {f.ArrivalAirportId} does not exist.");

            // All good – add flight
            _db.Flights.Add(f);
            _db.SaveChanges();
            return Ok(f);
        }


        // DELETE: api/flights/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlight(int id)
        {
            var flight = await _db.Flights.FindAsync(id);
            if (flight == null)
            {
                return NotFound();
            }

            _db.Flights.Remove(flight);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
