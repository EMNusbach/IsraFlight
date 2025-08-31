using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using IsraFlight.Api.Data;
using IsraFlight.Api.Models;

namespace IsraFlight.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TicketsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public TicketsController(AppDbContext db) { _db = db; }

        // GET: api/tickets
        [HttpGet]
        public IEnumerable<Ticket> Get() => _db.Tickets.ToList();

        // GET: api/tickets/{id}
        [HttpGet("{id}")]
        public async Task<ActionResult<Ticket>> GetTicket(int id)
        {
            var ticket = await _db.Tickets.FindAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            return ticket;
        }

        // PUT: api/tickets/{id}
        [HttpPut("{id}")]
        public async Task<IActionResult> PutTicket(int id, Ticket ticket)
        {
            if (id != ticket.Id)
            {
                return BadRequest("ID mismatch");
            }

            _db.Entry(ticket).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Tickets.Any(t => t.Id == id))
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

        // POST: api/tickets
        [HttpPost]
        public async Task<IActionResult> CreateTicket(Ticket t)
        {
            // Check that the flight exists
            var flight = await _db.Flights.FindAsync(t.FlightId);
            if (flight == null)
                return NotFound("Flight not found.");

            _db.Tickets.Add(t);
            await _db.SaveChangesAsync();

            return Ok(t);
        }

        // DELETE: api/tickets/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTicket(int id)
        {
            var ticket = await _db.Tickets.FindAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }

            _db.Tickets.Remove(ticket);
            await _db.SaveChangesAsync();

            return CreatedAtAction(nameof(GetTicket), new { id = ticket.Id }, ticket);
            //return NoContent();
        }
    }
}
