"""
Google Maps Company Scraper - Main Entry Point
Scrapes business information from Google Maps based on location and industry.
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime

from scraper import scrape_companies
from csv_exporter import CSVExporter


def setup_logging(verbose: bool = False):
    """
    Set up logging configuration.

    Args:
        verbose: Enable verbose logging (DEBUG level)
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create logs directory if it doesn't exist
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging
    log_filename = f'logs/scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
    logger.info(f"Log file: {log_filename}")


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Scrape company information from Google Maps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py --country "USA" --city "New York" --industry "restaurants"
  python main.py --country "USA" --city "Los Angeles" --industry "plumbers" --max-results 100
  python main.py --country "Canada" --city "Toronto" --industry "dentists" --output my_companies.csv
        '''
    )

    parser.add_argument(
        '--country',
        type=str,
        required=True,
        help='Country name (e.g., "USA", "Canada", "UK")'
    )

    parser.add_argument(
        '--city',
        type=str,
        required=True,
        help='City or region name (e.g., "New York", "Los Angeles")'
    )

    parser.add_argument(
        '--industry',
        type=str,
        required=True,
        help='Industry or business type (e.g., "restaurants", "plumbers", "dentists")'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=50,
        help='Maximum number of results to scrape (default: 50)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output CSV filename (default: auto-generated with timestamp)'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )

    parser.add_argument(
        '--visible',
        action='store_true',
        help='Run browser in visible mode (shows browser window)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()


async def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()

    # Set up logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)

    # Determine headless mode
    headless = not args.visible

    # Display configuration
    print("\n" + "="*60)
    print("Google Maps Company Scraper")
    print("="*60)
    print(f"Country:      {args.country}")
    print(f"City:         {args.city}")
    print(f"Industry:     {args.industry}")
    print(f"Max Results:  {args.max_results}")
    print(f"Browser Mode: {'Headless' if headless else 'Visible'}")
    print("="*60 + "\n")

    try:
        # Run the scraper
        logger.info("Starting scraping process...")
        print("🔍 Searching Google Maps...")

        businesses = await scrape_companies(
            country=args.country,
            city=args.city,
            industry=args.industry,
            max_results=args.max_results,
            headless=headless
        )

        # Export to CSV
        if businesses:
            print(f"\n✓ Successfully scraped {len(businesses)} businesses")
            print("📝 Exporting to CSV...")

            exporter = CSVExporter()
            output_file = exporter.export_to_csv(businesses, filename=args.output)

            # Display summary
            if output_file:
                summary = exporter.get_summary(output_file)
                print("\n" + "="*60)
                print("Summary:")
                print("="*60)
                print(f"Total records:          {summary.get('total_records', 0)}")
                print(f"Records with phone:     {summary.get('records_with_phone', 0)}")
                print(f"Records with website:   {summary.get('records_with_website', 0)}")
                print("="*60 + "\n")

            logger.info("Scraping completed successfully")
        else:
            print("\n⚠ No businesses found. Try adjusting your search parameters.")
            logger.warning("No businesses found")

    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
        logger.info("Scraping interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error(f"Scraping failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
