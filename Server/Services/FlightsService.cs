using System.Net.Http;
using System.Text.Json;
using Microsoft.Extensions.Configuration;

namespace Server.Services
{
    public class FlightArrivalDto
    {
        public string? FlightNumber { get; set; }
        public string? Airline { get; set; }
        public string? Origin { get; set; }
        public DateTime? ScheduledArrival { get; set; }
        public string? Terminal { get; set; }
        public string? Gate { get; set; }
        public string? Status { get; set; }
        public bool IsCodeshare { get; set; }
        public string? CodeshareAirline { get; set; }
        public string? CodeshareFlightNumber { get; set; }
    }

    public class FlightsService
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _config;

        public FlightsService(HttpClient httpClient, IConfiguration config)
        {
            _httpClient = httpClient;
            _config = config;
        }

        public async Task<List<FlightArrivalDto>> GetArrivalsAsync(
            int hoursAhead,
            string airportCode = "TLV",
            bool useIata = true,
            DateTime? flightDate = null)
        {
            if (hoursAhead < 1 || hoursAhead > 5)
                throw new ArgumentOutOfRangeException(nameof(hoursAhead), "Hours must be between 1 and 5.");

            var apiKey = _config["Aviationstack:ApiKey"];
            var baseUrl = _config["Aviationstack:BaseUrl"];

            var codeParam = useIata ? "arr_iata" : "arr_icao";
            var url = $"{baseUrl}/flights?access_key={apiKey}&{codeParam}={airportCode}";

            if (flightDate.HasValue)
                url += $"&flight_date={flightDate.Value:yyyy-MM-dd}";

            var response = await _httpClient.GetAsync(url);
            var json = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"[DEBUG] API Response: {json}");

            if (!response.IsSuccessStatusCode)
                throw new Exception($"Aviationstack API call failed: {json}");

            using var doc = JsonDocument.Parse(json);
            var flights = new List<FlightArrivalDto>();

            if (!doc.RootElement.TryGetProperty("data", out var data))
                return flights;

            // Calculate time window for filtering
            var now = DateTime.Now;
            var endTime = now.AddHours(hoursAhead);

            Console.WriteLine($"[DEBUG] Filtering flights from {now:yyyy-MM-dd HH:mm} to {endTime:yyyy-MM-dd HH:mm}");

            foreach (var item in data.EnumerateArray())
            {
                try
                {
                    var flightDto = ExtractFlightData(item);
                    if (flightDto != null && ShouldIncludeFlight(flightDto, now, endTime))
                    {
                        flights.Add(flightDto);
                        Console.WriteLine($"[DEBUG] Added flight: {flightDto.FlightNumber} from {flightDto.Origin} - {flightDto.ScheduledArrival} - {flightDto.Status}");
                    }
                    else if (flightDto != null)
                    {
                        Console.WriteLine($"[DEBUG] Excluded flight: {flightDto.FlightNumber} - {flightDto.ScheduledArrival} (outside time window)");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[DEBUG] Error processing flight item: {ex.Message}");
                }
            }

            // Sort by scheduled arrival time
            flights = flights.OrderBy(f => f.ScheduledArrival).ToList();

            Console.WriteLine($"[DEBUG] Returning {flights.Count} filtered flights");
            return flights;
        }

        private bool ShouldIncludeFlight(FlightArrivalDto flight, DateTime now, DateTime endTime)
        {
            if (!flight.ScheduledArrival.HasValue)
            {
                Console.WriteLine($"[DEBUG] Flight {flight.FlightNumber} has no scheduled arrival time - excluding");
                return false;
            }

            var arrivalTime = flight.ScheduledArrival.Value;
            
            // Include flights arriving from now until the specified hours ahead
            // Allow some buffer for flights that might be slightly in the past (e.g., 30 minutes)
            var bufferTime = now.AddMinutes(-30);
            var isInTimeWindow = arrivalTime >= bufferTime && arrivalTime <= endTime;

            Console.WriteLine($"[DEBUG] Flight {flight.FlightNumber}: Arrival={arrivalTime:HH:mm}, Window={bufferTime:HH:mm}-{endTime:HH:mm}, Include={isInTimeWindow}");
            
            return isInTimeWindow;
        }

        private string ExtractFlightNumber(JsonElement item)
        {
            if (item.TryGetProperty("flight", out var flightObj) &&
                flightObj.TryGetProperty("iata", out var flightNum))
            {
                return flightNum.GetString() ?? "Unknown Flight";
            }
            return "Unknown Flight";
        }

        private string ExtractAirlineName(JsonElement item)
        {
            if (item.TryGetProperty("airline", out var airlineObj) &&
                airlineObj.TryGetProperty("name", out var airlineName))
            {
                return airlineName.GetString() ?? "Unknown Airline";
            }
            return "Unknown Airline";
        }

        private string ExtractOrigin(JsonElement item)
        {
            if (item.TryGetProperty("departure", out var departureObj) &&
                departureObj.TryGetProperty("airport", out var origin))
            {
                return origin.GetString() ?? "Unknown Airport";
            }
            return "Unknown Airport";
        }

        private DateTime? ExtractScheduledArrival(JsonElement item)
        {
            if (item.TryGetProperty("arrival", out var arrivalObj) &&
                arrivalObj.TryGetProperty("scheduled", out var scheduledArrival) &&
                DateTime.TryParse(scheduledArrival.GetString(), out var parsedDate))
            {
                return parsedDate;
            }
            return null;
        }

        private string ExtractTerminal(JsonElement item)
        {
            if (item.TryGetProperty("arrival", out var arrivalObj) &&
                arrivalObj.TryGetProperty("terminal", out var terminal))
            {
                return terminal.GetString() ?? "N/A";
            }
            return "N/A";
        }

        private string ExtractGate(JsonElement item)
        {
            if (item.TryGetProperty("arrival", out var arrivalObj) &&
                arrivalObj.TryGetProperty("gate", out var gate))
            {
                return gate.GetString() ?? "N/A";
            }
            return "N/A";
        }

        private string ExtractStatus(JsonElement item)
        {
            if (item.TryGetProperty("flight_status", out var status))
            {
                return status.GetString() ?? "Unknown";
            }
            return "Unknown";
        }

        private (bool, string?, string?) ExtractCodeshareInfo(JsonElement item)
        {
            if (item.TryGetProperty("codeshared", out var codeshareObj))
            {
                string? airline = null;
                string? flightNumber = null;

                if (codeshareObj.TryGetProperty("airline", out var airlineObj) &&
                    airlineObj.TryGetProperty("name", out var csAirlineName))
                {
                    airline = csAirlineName.GetString();
                }

                if (codeshareObj.TryGetProperty("flight", out var flightObj) &&
                    flightObj.TryGetProperty("iata", out var csFlightNum))
                {
                    flightNumber = csFlightNum.GetString();
                }

                return (true, airline, flightNumber);
            }

            return (false, null, null);
        }

        private FlightArrivalDto? ExtractFlightData(JsonElement item)
        {
            try
            {
                var (isCodeshare, csAirline, csFlightNumber) = ExtractCodeshareInfo(item);

                return new FlightArrivalDto
                {
                    FlightNumber = isCodeshare && !string.IsNullOrEmpty(csFlightNumber)
                        ? csFlightNumber
                        : ExtractFlightNumber(item),
                    Airline = isCodeshare && !string.IsNullOrEmpty(csAirline)
                        ? csAirline
                        : ExtractAirlineName(item),
                    Origin = ExtractOrigin(item),
                    ScheduledArrival = ExtractScheduledArrival(item),
                    Terminal = ExtractTerminal(item),
                    Gate = ExtractGate(item),
                    Status = ExtractStatus(item),
                    IsCodeshare = isCodeshare,
                    CodeshareAirline = csAirline,
                    CodeshareFlightNumber = csFlightNumber
                };
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] ExtractFlightData: {ex.Message}");
                return null;
            }
        }
    }
}