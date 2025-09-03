using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;

namespace Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AirportsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public AirportsController(AppDbContext db) { _db = db; }

        // GET: api/airports
        [HttpGet]
        public IEnumerable<Airport> Get() => _db.Airports.ToList();

        // GET: api/airports/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Airport>> GetAirport(int id)
        {
            var airport = await _db.Airports.FindAsync(id);
            if (airport == null)
            {
                return NotFound();
            }
            return airport;
        }

        // PUT: api/airports/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutAirport(int id, Airport airport)
        {
            if (id != airport.Id)
            {
                return BadRequest("ID mismatch");
            }

            _db.Entry(airport).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Airports.Any(a => a.Id == id))
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

        // POST: api/airports
        [HttpPost]
        public IActionResult Post(Airport a)
        {
            _db.Airports.Add(a);
            _db.SaveChanges();
            return Ok(a);
        }

        // DELETE: api/airports/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAirport(int id)
        {
            var airport = await _db.Airports.FindAsync(id);
            if (airport == null)
            {
                return NotFound();
            }

            _db.Airports.Remove(airport);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
