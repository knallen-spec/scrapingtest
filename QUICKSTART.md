# Quick Start Guide

Get up and running with the Google Maps Company Scraper in 5 minutes!

## Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

## Step 2: Run Your First Scrape

```bash
python main.py --country "USA" --city "New York" --industry "coffee shops" --max-results 20
```

This will:
1. Search Google Maps for "coffee shops in New York, USA"
2. Extract up to 20 business listings
3. Save results to `output/companies_YYYYMMDD_HHMMSS.csv`
4. Save logs to `logs/scraper_YYYYMMDD_HHMMSS.log`

## Step 3: View Your Results

```bash
# The output file will be in the output directory
ls output/

# View the CSV (on Linux/Mac)
cat output/companies_*.csv

# Or open it in Excel, Google Sheets, etc.
```

## Common Use Cases

### Scrape Local Service Businesses

```bash
# Plumbers
python main.py --country "USA" --city "Chicago" --industry "plumbers"

# Dentists
python main.py --country "USA" --city "Los Angeles" --industry "dentists"

# Electricians
python main.py --country "USA" --city "Houston" --industry "electricians"
```

### Scrape Restaurants and Food

```bash
# Pizza restaurants
python main.py --country "USA" --city "New York" --industry "pizza restaurants"

# Mexican restaurants
python main.py --country "USA" --city "San Diego" --industry "mexican restaurants"
```

### Scrape Retail Stores

```bash
# Clothing stores
python main.py --country "USA" --city "Miami" --industry "clothing stores"

# Pet stores
python main.py --country "USA" --city "Seattle" --industry "pet stores"
```

## Tips for Success

1. **Be Specific**: Use specific industry terms like "italian restaurants" instead of just "restaurants"
2. **Start Small**: Begin with `--max-results 20` to test before scaling up
3. **Check Logs**: If something goes wrong, check the log files in the `logs/` directory
4. **Use Visible Mode**: Add `--visible` flag to watch the browser in action for debugging

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Adjust the scraper code in `scraper.py` to extract additional fields
- Modify `csv_exporter.py` to change the output format
- Add your own features!

## Need Help?

If you encounter issues:
1. Check the `logs/` directory for error messages
2. Try running with `--visible` to see what's happening
3. Reduce `--max-results` if the scraper is timing out
4. Make sure you've installed Playwright browsers: `playwright install chromium`
