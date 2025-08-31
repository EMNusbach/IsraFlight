using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using IsraFlight.Api.Data;
using IsraFlight.Api.Models;

namespace IsraFlight.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FrequentFlyersController : ControllerBase
    {
        private readonly AppDbContext _db;
        public FrequentFlyersController(AppDbContext db) { _db = db; }

        // GET: api/FrequentFlyers
        [HttpGet]
        public IEnumerable<FrequentFlyer> Get() => _db.FrequentFlyers.ToList();

        // GET: api/FrequentFlyerrs/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            var FrequentFlyer= await _db.FrequentFlyers.FindAsync(id);
            if (FrequentFlyer == null)
            {
                return NotFound();
            }
            return FrequentFlyer;
        }

        // PUT: api/FrequentFlyers/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFrequentFlyer(int id, FrequentFlyer frequentFlyer)
        {
            if (id != frequentFlyer.Id)
            {
                return BadRequest("ID mismatch");
            }

            _db.Entry(frequentFlyer).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.FrequentFlyers.Any(f => f.Id == id))
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

        // POST: api/FrequentFlyers
        [HttpPost]
        public IActionResult Post(FrequentFlyer f)
        {
            // Check unique username
            var usernameTaken = _db.FrequentFlyers.Any(ff => ff.Username == f.Username);
            if (usernameTaken)
                return BadRequest($"Username '{f.Username}' is already taken.");

            _db.FrequentFlyers.Add(f);
            _db.SaveChanges();
            return Ok(f);
        }


        // DELETE: api/FrequentFlyers/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFrequentFlyer(int id)
        {
            var frequentFlyer = await _db.FrequentFlyers.FindAsync(id);
            if (frequentFlyer == null)
            {
                return NotFound();
            }

            _db.FrequentFlyers.Remove(frequentFlyer);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
