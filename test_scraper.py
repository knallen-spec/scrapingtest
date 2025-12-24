"""
Test script to verify the scraper setup and demonstrate functionality.
This script validates the code structure without requiring browser downloads.
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from csv_exporter import CSVExporter


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import scraper
        import csv_exporter
        import main
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_csv_exporter():
    """Test CSV export functionality."""
    print("\nTesting CSV exporter...")
    try:
        # Sample data
        sample_data = [
            {
                'company_name': 'Test Coffee Shop',
                'phone_number': '+1-212-555-0100',
                'website': 'https://testcoffee.com',
                'owner_first_name': '',
                'owner_last_name': '',
                'location': '123 Main St, New York, NY 10001',
                'industry': 'coffee shops',
                'city': 'New York',
                'country': 'USA'
            },
            {
                'company_name': 'Another Cafe',
                'phone_number': '+1-212-555-0101',
                'website': 'https://anothercafe.com',
                'owner_first_name': '',
                'owner_last_name': '',
                'location': '456 Broadway, New York, NY 10002',
                'industry': 'coffee shops',
                'city': 'New York',
                'country': 'USA'
            }
        ]

        # Create exporter
        exporter = CSVExporter(output_dir='test_output')

        # Export data
        output_file = exporter.export_to_csv(sample_data, filename='test_sample.csv')

        if output_file and os.path.exists(output_file):
            print(f"✓ CSV exported successfully to {output_file}")

            # Get summary
            summary = exporter.get_summary(output_file)
            print(f"  - Total records: {summary['total_records']}")
            print(f"  - Records with phone: {summary['records_with_phone']}")
            print(f"  - Records with website: {summary['records_with_website']}")

            # Read and display
            import pandas as pd
            df = pd.read_csv(output_file)
            print(f"\n  Sample output (first 2 rows):")
            print(df.head(2).to_string(index=False))

            return True
        else:
            print("✗ CSV export failed")
            return False

    except Exception as e:
        print(f"✗ CSV export test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scraper_initialization():
    """Test scraper can be initialized (without running)."""
    print("\nTesting scraper initialization...")
    try:
        from scraper import GoogleMapsScraper

        scraper = GoogleMapsScraper(headless=True)
        print("✓ Scraper initialized successfully")
        print(f"  - Headless mode: {scraper.headless}")
        return True

    except Exception as e:
        print(f"✗ Scraper initialization failed: {e}")
        return False


def test_argument_parsing():
    """Test command-line argument parsing."""
    print("\nTesting argument parsing...")
    try:
        # Temporarily modify sys.argv
        original_argv = sys.argv.copy()
        sys.argv = [
            'main.py',
            '--country', 'USA',
            '--city', 'New York',
            '--industry', 'restaurants',
            '--max-results', '50'
        ]

        from main import parse_arguments
        args = parse_arguments()

        assert args.country == 'USA'
        assert args.city == 'New York'
        assert args.industry == 'restaurants'
        assert args.max_results == 50

        print("✓ Argument parsing works correctly")
        print(f"  - Country: {args.country}")
        print(f"  - City: {args.city}")
        print(f"  - Industry: {args.industry}")
        print(f"  - Max results: {args.max_results}")

        # Restore original argv
        sys.argv = original_argv
        return True

    except Exception as e:
        print(f"✗ Argument parsing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.argv = original_argv
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Google Maps Scraper - Test Suite")
    print("="*60)

    results = []

    # Run tests
    results.append(('Module Imports', test_imports()))
    results.append(('Scraper Initialization', test_scraper_initialization()))
    results.append(('Argument Parsing', test_argument_parsing()))
    results.append(('CSV Export', test_csv_exporter()))

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The scraper is ready to use.")
        print("\nNote: To run the actual scraper, you need to:")
        print("  1. Install Playwright browser: playwright install chromium")
        print("  2. Run: python main.py --country \"USA\" --city \"New York\" --industry \"restaurants\"")
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")

    print("="*60)


if __name__ == "__main__":
    main()
