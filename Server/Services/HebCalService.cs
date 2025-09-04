using System.Net.Http;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using System.Globalization;

public class HebCalService
{
    private readonly HttpClient _http;

    public HebCalService(HttpClient http)
    {
        _http = http;
    }

    // Returns whether the date is Shabbat, the parasha, and Shabbat entry/exit times
    public async Task<(bool isShabbat, string parasha, DateTime entryTime, DateTime exitTime)> GetShabbatInfo(DateTime landingTime)
    {
        // We're using Jerusalem by default (GeoName ID = 281184)
        string url = $"https://www.hebcal.com/shabbat?cfg=json&geonameid=281184&start={landingTime.AddDays(-1):yyyy-MM-dd}&end={landingTime.AddDays(1):yyyy-MM-dd}";

        var response = await _http.GetAsync(url);
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        
        // Configure JsonSerializer options for property name handling
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
        
        var hebcalData = JsonSerializer.Deserialize<HebCalResponse>(json, options);

        bool isShabbat = false;
        string parasha = "";
        DateTime entryTime = DateTime.MinValue;
        DateTime exitTime = DateTime.MinValue;

        if (hebcalData?.Items != null)
        {
            foreach (var item in hebcalData.Items)
            {
                // Get parasha name
                if (item.Category == "parashat" && string.IsNullOrEmpty(parasha))
                {
                    parasha = item.Hebrew ?? item.Title ?? "";
                }

                // Shabbat entry (candle lighting)
                if (item.Category == "candles" && entryTime == DateTime.MinValue)
                {
                    if (DateTime.TryParse(item.Date, CultureInfo.InvariantCulture, DateTimeStyles.RoundtripKind, out var parsedEntry))
                    {
                        entryTime = parsedEntry;
                    }
                }

                // Shabbat exit (havdalah)
                if (item.Category == "havdalah" && exitTime == DateTime.MinValue)
                {
                    if (DateTime.TryParse(item.Date, CultureInfo.InvariantCulture, DateTimeStyles.RoundtripKind, out var parsedExit))
                    {
                        exitTime = parsedExit;
                    }
                }
            }
        }

        // Is landing time during Shabbat? Between candle lighting and havdalah
        if (entryTime != DateTime.MinValue && exitTime != DateTime.MinValue)
        {
            isShabbat = landingTime >= entryTime && landingTime <= exitTime;
        }

        return (isShabbat, parasha, entryTime, exitTime);
    }
}

// Response models for HebCal 
public class HebCalResponse
{
    [JsonPropertyName("items")]
    public List<HebCalItem> Items { get; set; } = new List<HebCalItem>();
}

public class HebCalItem
{
    [JsonPropertyName("title")]
    public string? Title { get; set; }

    [JsonPropertyName("hebrew")]
    public string? Hebrew { get; set; }

    [JsonPropertyName("category")]
    public string? Category { get; set; }

    [JsonPropertyName("date")]
    public string? Date { get; set; }
}