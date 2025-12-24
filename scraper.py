"""
Google Maps Company Scraper
Scrapes business information from Google Maps based on location and industry.
"""

import asyncio
import logging
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
import time


class GoogleMapsScraper:
    """Scraper for Google Maps business listings."""

    def __init__(self, headless: bool = True):
        """
        Initialize the scraper.

        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.logger = logging.getLogger(__name__)

    async def setup(self):
        """Set up the browser and page."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.logger.info("Browser launched successfully")

    async def teardown(self):
        """Close the browser and clean up."""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        self.logger.info("Browser closed")

    async def search_google_maps(self, country: str, city: str, industry: str, max_results: int = 50) -> List[Dict]:
        """
        Search Google Maps for businesses and extract information.

        Args:
            country: Country name
            city: City or region name
            industry: Industry/business type
            max_results: Maximum number of results to scrape

        Returns:
            List of dictionaries containing business information
        """
        # Construct search query
        search_query = f"{industry} in {city}, {country}"
        self.logger.info(f"Searching for: {search_query}")

        # Create new page
        page = await self.browser.new_page()

        # Set viewport and user agent to avoid detection
        await page.set_viewport_size({"width": 1920, "height": 1080})

        try:
            # Navigate to Google Maps
            google_maps_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            await page.goto(google_maps_url, wait_until="networkidle", timeout=60000)

            # Wait for results to load
            await page.wait_for_timeout(3000)

            # Scroll to load more results
            await self._scroll_results(page, max_results)

            # Extract business listings
            businesses = await self._extract_businesses(page, country, city, industry, max_results)

            return businesses

        except Exception as e:
            self.logger.error(f"Error during search: {str(e)}")
            raise
        finally:
            await page.close()

    async def _scroll_results(self, page: Page, max_results: int):
        """
        Scroll through the results panel to load more listings.

        Args:
            page: Playwright page object
            max_results: Maximum number of results to load
        """
        self.logger.info("Scrolling to load results...")

        # Find the scrollable results container
        scrollable_section = page.locator('div[role="feed"]').first

        previous_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 20

        while scroll_attempts < max_scroll_attempts:
            # Scroll to bottom of the results panel
            await scrollable_section.evaluate("element => element.scrollTo(0, element.scrollHeight)")
            await page.wait_for_timeout(2000)

            # Count current results
            current_count = await page.locator('div[role="feed"] > div').count()

            self.logger.info(f"Loaded {current_count} results")

            # Check if we've reached the target or no new results loaded
            if current_count >= max_results or current_count == previous_count:
                break

            previous_count = current_count
            scroll_attempts += 1

    async def _extract_businesses(self, page: Page, country: str, city: str, industry: str, max_results: int) -> List[Dict]:
        """
        Extract business information from the loaded results.

        Args:
            page: Playwright page object
            country: Country name
            city: City or region name
            industry: Industry/business type
            max_results: Maximum number of results to extract

        Returns:
            List of business dictionaries
        """
        businesses = []

        # Get all business listing elements
        listings = page.locator('div[role="feed"] > div').all()

        self.logger.info(f"Extracting data from {len(await listings)} listings...")

        count = 0
        for listing in await listings:
            if count >= max_results:
                break

            try:
                # Click on the listing to open details
                await listing.click()
                await page.wait_for_timeout(2000)

                # Extract business data
                business_data = await self._extract_business_details(page, country, city, industry)

                if business_data:
                    businesses.append(business_data)
                    count += 1
                    self.logger.info(f"Extracted: {business_data.get('company_name', 'Unknown')}")

            except Exception as e:
                self.logger.warning(f"Failed to extract business {count + 1}: {str(e)}")
                continue

        return businesses

    async def _extract_business_details(self, page: Page, country: str, city: str, industry: str) -> Optional[Dict]:
        """
        Extract detailed information from a business listing.

        Args:
            page: Playwright page object
            country: Country name
            city: City or region name
            industry: Industry/business type

        Returns:
            Dictionary with business information or None if extraction fails
        """
        try:
            business_data = {
                'company_name': '',
                'phone_number': '',
                'website': '',
                'owner_first_name': '',  # Not available on Google Maps
                'owner_last_name': '',   # Not available on Google Maps
                'location': '',
                'industry': industry,
                'country': country,
                'city': city
            }

            # Extract company name
            try:
                name_element = page.locator('h1.DUwDvf').first
                business_data['company_name'] = await name_element.inner_text(timeout=5000)
            except:
                self.logger.warning("Could not extract company name")

            # Extract phone number
            try:
                phone_button = page.locator('button[data-item-id*="phone:tel:"]').first
                phone_text = await phone_button.get_attribute('data-item-id', timeout=5000)
                if phone_text:
                    business_data['phone_number'] = phone_text.split('tel:')[-1]
            except:
                self.logger.debug("Phone number not available")

            # Extract website
            try:
                website_link = page.locator('a[data-item-id="authority"]').first
                business_data['website'] = await website_link.get_attribute('href', timeout=5000)
            except:
                self.logger.debug("Website not available")

            # Extract address
            try:
                address_button = page.locator('button[data-item-id="address"]').first
                business_data['location'] = await address_button.inner_text(timeout=5000)
            except:
                self.logger.debug("Address not available")

            return business_data

        except Exception as e:
            self.logger.error(f"Error extracting business details: {str(e)}")
            return None


async def scrape_companies(country: str, city: str, industry: str, max_results: int = 50, headless: bool = True) -> List[Dict]:
    """
    Main function to scrape companies from Google Maps.

    Args:
        country: Country name
        city: City or region name
        industry: Industry/business type
        max_results: Maximum number of results to scrape (default: 50)
        headless: Run browser in headless mode (default: True)

    Returns:
        List of dictionaries containing business information
    """
    scraper = GoogleMapsScraper(headless=headless)

    try:
        await scraper.setup()
        businesses = await scraper.search_google_maps(country, city, industry, max_results)
        return businesses
    finally:
        await scraper.teardown()
