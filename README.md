# Google Maps Company Scraper

A Python-based web scraper that extracts company information from Google Maps based on location and industry.

## Features

- 🔍 Scrape companies from Google Maps by country, city/region, and industry
- 📊 Extract: Company name, phone number, website, location, and industry
- 💾 Export results to CSV format
- 🤖 Headless browser automation using Playwright
- 📝 Detailed logging and error handling
- ⚙️ Customizable result limits

## Installation

1. **Clone the repository** (if not already done):
```bash
git clone <repository-url>
cd scrapingtest
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**:
```bash
playwright install chromium
```

## Usage

### Basic Usage

```bash
python main.py --country "USA" --city "New York" --industry "restaurants"
```

### Advanced Usage

**Scrape more results:**
```bash
python main.py --country "USA" --city "Los Angeles" --industry "plumbers" --max-results 100
```

**Custom output filename:**
```bash
python main.py --country "Canada" --city "Toronto" --industry "dentists" --output my_dentists.csv
```

**Run with visible browser (for debugging):**
```bash
python main.py --country "USA" --city "Miami" --industry "hotels" --visible
```

**Enable verbose logging:**
```bash
python main.py --country "UK" --city "London" --industry "restaurants" --verbose
```

### Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--country` | Yes | Country name | `"USA"`, `"Canada"`, `"UK"` |
| `--city` | Yes | City or region name | `"New York"`, `"Los Angeles"` |
| `--industry` | Yes | Industry or business type | `"restaurants"`, `"plumbers"` |
| `--max-results` | No | Maximum number of results (default: 50) | `100` |
| `--output` | No | Custom output filename | `"my_companies.csv"` |
| `--visible` | No | Run browser in visible mode | - |
| `--verbose` or `-v` | No | Enable verbose logging | - |

## Output

### CSV File Structure

Results are saved to `output/companies_{timestamp}.csv` with the following columns:

- `company_name` - Name of the business
- `phone_number` - Contact phone number
- `website` - Company website URL
- `owner_first_name` - Owner's first name (not available from Google Maps)
- `owner_last_name` - Owner's last name (not available from Google Maps)
- `location` - Full address
- `industry` - Industry category (as specified in search)
- `city` - City/region (as specified in search)
- `country` - Country (as specified in search)

### Log Files

Detailed logs are saved to `logs/scraper_{timestamp}.log`

## Examples

**Scrape restaurants in New York:**
```bash
python main.py --country "USA" --city "New York" --industry "restaurants" --max-results 50
```

**Scrape plumbing companies in Chicago:**
```bash
python main.py --country "USA" --city "Chicago" --industry "plumbing services"
```

**Scrape dentists in Toronto with custom filename:**
```bash
python main.py --country "Canada" --city "Toronto" --industry "dentists" --output toronto_dentists.csv
```

## Important Notes

- **Owner Information**: Google Maps does not publicly display owner first/last names, so these fields will be empty in the CSV output.
- **Rate Limiting**: The scraper includes delays to avoid being blocked. Adjust `max_results` based on your needs.
- **Terms of Service**: Ensure you comply with Google's Terms of Service when using this tool.
- **Ethical Use**: Use this tool responsibly and respect privacy regulations.

## Project Structure

```
scrapingtest/
├── main.py              # Main entry point
├── scraper.py           # Google Maps scraper logic
├── csv_exporter.py      # CSV export functionality
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── output/             # CSV output files (created automatically)
└── logs/               # Log files (created automatically)
```

## Troubleshooting

**Browser not launching:**
- Make sure you've run `playwright install chromium`

**No results found:**
- Try adjusting your search query (industry name)
- Check if the location name is correct
- Try reducing `max-results` for initial testing

**Scraper getting blocked:**
- The scraper includes built-in delays, but you may need to reduce `max-results`
- Try running with `--visible` to see what's happening in the browser

## License

This project is for educational purposes only. Use responsibly and in accordance with applicable laws and terms of service.
