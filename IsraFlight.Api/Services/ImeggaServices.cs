using System.Net.Http.Headers;
using System.Text.Json;

public sealed class ImaggaService
{
    // Words to identify planes
    private static readonly string[] PlaneWords = { "airplane", "aircraft", "aeroplane", "plane", "jet", "airliner" };

    private readonly HttpClient _http;

    // Your API credentials (hardcoded)
    private readonly string _apiKey = "acc_077b22929334bf9";
    private readonly string _apiSecret = "1484e90a6ae6741e5df9a23403cc3ab6";
    private readonly double _minConfidence = 40.0;

    public ImaggaService()
    {
        _http = new HttpClient();

        // Basic auth for Imagga
        var auth = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes($"{_apiKey}:{_apiSecret}"));
        _http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", auth);
        _http.BaseAddress = new Uri("https://api.imagga.com/v2/");
        _http.Timeout = TimeSpan.FromSeconds(10);
    }

    public async Task<bool> IsPlaneImageUrlAsync(string imageUrl)
    {
        if (!Uri.TryCreate(imageUrl, UriKind.Absolute, out var uri) ||
            (uri.Scheme != Uri.UriSchemeHttp && uri.Scheme != Uri.UriSchemeHttps))
        {
            return false;
        }

        var resp = await _http.GetAsync($"tags?image_url={Uri.EscapeDataString(imageUrl)}");
        if (!resp.IsSuccessStatusCode)
        {
            return false;
        }

        var json = await resp.Content.ReadAsStringAsync();

        var data = JsonDocument.Parse(json);
        var tags = data.RootElement.GetProperty("result").GetProperty("tags");

        foreach (var tag in tags.EnumerateArray())
        {
            var confidence = tag.GetProperty("confidence").GetDouble();
            var label = tag.GetProperty("tag").GetProperty("en").GetString();

            if (confidence >= _minConfidence && PlaneWords.Any(w => string.Equals(w, label, StringComparison.OrdinalIgnoreCase)))
            {
                return true;
            }
        }

        return false;
    }
}

