using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;

namespace Server.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PlanesController : ControllerBase
    {
        private readonly AppDbContext _db;
        private readonly ImaggaService _imagga;

        // Constructor with dependencies injected
        public PlanesController(AppDbContext db)
        {
            _db = db;
            _imagga = new ImaggaService();
        }

        // GET: api/planes
        // Returns a list of all planes
        [HttpGet]
        public async Task<IEnumerable<Plane>> Get()
        {
            return await _db.Planes.ToListAsync();
        }

        // GET: api/planes/{id}
        // Returns a single plane by ID
        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(int id)
        {
            var plane = await _db.Planes.FindAsync(id);
            if (plane == null)
                return NotFound();

            return Ok(plane);
        }

        // POST: api/planes
        // Creates a new plane after validating fields and image
        [HttpPost]
        public async Task<IActionResult> Create([FromBody] Plane p)
        {
            // Basic field validation
            if (string.IsNullOrWhiteSpace(p.Manufacturer) ||
                string.IsNullOrWhiteSpace(p.Nickname) ||
                p.Year < 1950 ||
                string.IsNullOrWhiteSpace(p.ImageUrl))
            {
                return BadRequest("Missing or invalid fields.");
            }

            // Validate that the image URL is actually a plane
            var looksLikePlane = await _imagga.IsPlaneImageUrlAsync(p.ImageUrl);
            if (!looksLikePlane)
                return BadRequest("The image does not appear to be a plane.");

            // Create a new plane object
            var plane = new Plane
            {
                Manufacturer = p.Manufacturer,
                Nickname = p.Nickname,
                Year = p.Year,
                ImageUrl = p.ImageUrl
            };

            // Save to the database
            _db.Planes.Add(plane);
            await _db.SaveChangesAsync();

            // Return 201 Created with location header
            return CreatedAtAction(nameof(GetById), new { id = plane.Id }, plane);
        }

        // PUT: api/planes/{id}
        // Updates an existing plane
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePlane(int id, [FromBody] Plane updatedPlane)
        {
            if (id != updatedPlane.Id)
                return BadRequest("ID mismatch.");

            // Find the existing plane
            var existingPlane = await _db.Planes.FindAsync(id);
            if (existingPlane == null)
                return NotFound();

            // If the image was changed, validate the new image
            if (!string.Equals(existingPlane.ImageUrl, updatedPlane.ImageUrl, StringComparison.OrdinalIgnoreCase))
            {
                var isPlane = await _imagga.IsPlaneImageUrlAsync(updatedPlane.ImageUrl);
                if (!isPlane)
                    return BadRequest("The new image does not appear to be a plane.");
            }

            // Update the plane fields
            existingPlane.Manufacturer = updatedPlane.Manufacturer;
            existingPlane.Nickname = updatedPlane.Nickname;
            existingPlane.Year = updatedPlane.Year;
            existingPlane.ImageUrl = updatedPlane.ImageUrl;

            // Save changes to the database
            try
            {
                await _db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!await _db.Planes.AnyAsync(p => p.Id == id))
                    return NotFound();
                else
                    throw;
            }

            return NoContent(); // 204 No Content on successful update
        }

        // DELETE: api/planes/{id}
        // Deletes a plane by ID
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePlane(int id)
        {
            var plane = await _db.Planes.FindAsync(id);
            if (plane == null)
                return NotFound();

            _db.Planes.Remove(plane);
            await _db.SaveChangesAsync();

            return NoContent(); // 204 No Content on successful deletion
        }
    }
}
