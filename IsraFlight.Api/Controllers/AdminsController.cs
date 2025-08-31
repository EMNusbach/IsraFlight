using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using IsraFlight.Api.Data;
using IsraFlight.Api.Models;

namespace IsraFlight.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AdminsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public AdminsController(AppDbContext db) { _db = db; }

        // GET: api/admins
        [HttpGet]
        public IEnumerable<Admin> Get() => _db.Admins.ToList();

        // GET: api/admins/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Admin>> GetAdmin(int id)
        {
            var admin = await _db.Admins.FindAsync(id);
            if (admin == null)
            {
                return NotFound();
            }
            return admin;
        }

        // PUT: api/admins/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutAdmin(int id, Admin admin)
        {
            if (id != admin.Id)
            {
                return BadRequest("Id mismatch");
            }

            _db.Entry(admin).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Admins.Any(a => a.Id == id))
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

        // POST: api/admins
        [HttpPost]
        public IActionResult Post(Admin a)
        {
            _db.Admins.Add(a);
            _db.SaveChanges();
            return Ok(a);
        }

        // DELETE: api/admins/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAdmin(int id)
        {
            var admin = await _db.Admins.FindAsync(id);
            if (admin == null)
            {
                return NotFound();
            }

            _db.Admins.Remove(admin);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
