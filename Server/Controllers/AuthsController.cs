using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;

namespace Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public AuthsController(AppDbContext db) { _db = db; }

        // GET: api/auths
        [HttpGet]
        public IEnumerable<Auth> Get() => _db.Auths.ToList();

        // GET: api/auths/5
        [HttpGet("{id:int}")]
        public async Task<ActionResult<Auth>> GetAuth(int id)
        {
            var auth = await _db.Auths.FindAsync(id);
            if (auth == null)
            {
                return NotFound();
            }
            return auth;
        }

        // PUT: api/auths/5
        [HttpPut("{id:int}")]
        public async Task<IActionResult> PutAuth(int id, Auth auth)
        {
            if (id != auth.Id)
            {
                return BadRequest("Id mismatch");
            }

            _db.Entry(auth).State = EntityState.Modified;

            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_db.Auths.Any(a => a.Id == id))
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

        // POST: api/auths
        [HttpPost]
        public IActionResult Post(Auth a)
        {
            _db.Auths.Add(a);
            _db.SaveChanges();
            return Ok(a);
        }

        // POST: api/auths/login
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] Auth credentials)
        {
            Console.WriteLine($"[LOGIN] Received login request for Username: {credentials.Username}");

            var user = await _db.Auths.FirstOrDefaultAsync(u =>
                u.Username == credentials.Username && u.Password == credentials.Password);

            if (user == null)
            {
                Console.WriteLine("[LOGIN] Invalid credentials.");
                return Unauthorized(new { error = "Invalid username or password" });
            }

            Console.WriteLine($"[LOGIN] Login successful. Returning user: {user.Username}, Role: {user.Role}");

            return Ok(new
            {
                auth = new
                {
                    Id = user.Id,
                    Username = user.Username,
                    Role = user.Role
                }
            });
        }


        // POST: api/auths/register
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] Auth newUser)
        {
            if (string.IsNullOrWhiteSpace(newUser.Username) ||
                string.IsNullOrWhiteSpace(newUser.Password))
            {
                return BadRequest(new { error = "Username and password are required." });
            }

            if (await _db.Auths.AnyAsync(u => u.Username == newUser.Username))
            {
                return Conflict(new { error = "Username already exists." });
            }

            _db.Auths.Add(newUser);
            await _db.SaveChangesAsync();

            return Ok(new
            {
                user = new
                {
                    id = newUser.Id,
                    username = newUser.Username,
                    role = newUser.Role,
                }
            });
        }


        // DELETE: api/auths/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAuth(int id)
        {
            var auth = await _db.Auths.FindAsync(id);
            if (auth == null)
            {
                return NotFound();
            }

            _db.Auths.Remove(auth);
            await _db.SaveChangesAsync();

            return NoContent();
        }
    }
}
