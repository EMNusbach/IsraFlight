using System.Net.Http;
using System.Text.Json;
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
        var hebcalData = JsonSerializer.Deserialize<HebCalResponse>(json);

        bool isShabbat = false;
        string parasha = "";
        DateTime entryTime = DateTime.MinValue;
        DateTime exitTime = DateTime.MinValue;

        foreach (var item in hebcalData.items)
        {
            // Get parasha name
            if (item.category == "parashat" && string.IsNullOrEmpty(parasha))
            {
                parasha = item.hebrew;
            }

            // Shabbat entry (candle lighting)
            if (item.category == "candles" && entryTime == DateTime.MinValue)
            {
                DateTime.TryParse(item.date, out entryTime);
            }

            // Shabbat exit (havdalah)
            if (item.category == "havdalah" && exitTime == DateTime.MinValue)
            {
                DateTime.TryParse(item.date, out exitTime);
            }
        }

        // Is landing time during Shabbat? Between candle lighting and havdalah
        if (entryTime != DateTime.MinValue && exitTime != DateTime.MinValue)
        {
            isShabbat = landingTime >= entryTime && landingTime <= exitTime;
        }

        return (isShabbat, parasha, entryTime, exitTime);
    }


    // Response models for HebCal
    public class HebCalResponse
    {
        public List<HebCalItem> items { get; set; }
    }

    public class HebCalItem
    {
        public string title { get; set; }
        public string hebrew { get; set; }
        public string category { get; set; }

        public string date { get; set; }
    }

}
