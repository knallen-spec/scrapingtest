"""
Streamlit Web Application for Google Maps Company Scraper
A user-friendly web interface for scraping company data from Google Maps.
"""

import streamlit as st
import pandas as pd
import asyncio
from datetime import datetime
import os
import io
import sys
import subprocess

# Install Playwright browsers on first run
@st.cache_resource
def setup_playwright():
    """Install Playwright browsers if not already installed."""
    try:
        cache_dir = os.path.expanduser("~/.cache/ms-playwright")
        if not os.path.exists(cache_dir) or not os.listdir(cache_dir):
            with st.spinner("Installing browser (first time setup, takes 2-3 minutes)..."):
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"])
                return True
        return True
    except Exception as e:
        st.error(f"Could not install browser: {e}")
        st.info("System dependencies are installed via packages-apt.txt")
        return False

# Run setup
setup_playwright()

from scraper import scrape_companies
from csv_exporter import CSVExporter


# Page configuration
st.set_page_config(
    page_title="Google Maps Company Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'scraping_results' not in st.session_state:
    st.session_state.scraping_results = None
if 'scraping_history' not in st.session_state:
    st.session_state.scraping_history = []
if 'is_scraping' not in st.session_state:
    st.session_state.is_scraping = False
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = None


def run_scraper(country, city, industry, max_results, headless=True):
    """Run the scraper and return results."""
    try:
        # Run async scraper
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            scrape_companies(country, city, industry, max_results, headless)
        )
        loop.close()
        return results
    except Exception as e:
        st.error(f"Error during scraping: {str(e)}")
        return None


def main():
    """Main application function."""

    # Header
    st.title("🔍 Google Maps Company Scraper")
    st.markdown("Extract company information from Google Maps based on location and industry")

    # Sidebar for input parameters
    st.sidebar.header("Search Parameters")

    with st.sidebar:
        country = st.text_input(
            "Country",
            value="USA",
            help="Enter the country name (e.g., USA, Canada, UK)"
        )

        city = st.text_input(
            "City or Region",
            value="New York",
            help="Enter the city or region name"
        )

        industry = st.text_input(
            "Industry",
            value="restaurants",
            help="Enter the industry or business type (e.g., restaurants, plumbers)"
        )

        max_results = st.slider(
            "Maximum Results",
            min_value=5,
            max_value=200,
            value=50,
            step=5,
            help="Maximum number of results to scrape"
        )

        headless = st.checkbox(
            "Headless Mode",
            value=True,
            help="Run browser in headless mode (recommended for cloud)"
        )

        st.markdown("---")

        # Start scraping button
        if st.button("🚀 Start Scraping", type="primary", use_container_width=True):
            if not country or not city or not industry:
                st.error("Please fill in all required fields!")
            else:
                st.session_state.is_scraping = True

    # Main content area
    if st.session_state.is_scraping:
        # Show scraping progress
        with st.spinner(f"Scraping {industry} in {city}, {country}..."):
            progress_text = st.empty()
            progress_bar = st.progress(0)

            progress_text.text("Initializing browser...")
            progress_bar.progress(10)

            progress_text.text("Loading Google Maps...")
            progress_bar.progress(30)

            progress_text.text("Extracting business data...")
            progress_bar.progress(50)

            # Run scraper
            results = run_scraper(country, city, industry, max_results, headless)

            progress_bar.progress(100)
            progress_text.text("Scraping completed!")

            if results:
                st.session_state.scraping_results = pd.DataFrame(results)
                st.session_state.edited_data = st.session_state.scraping_results.copy()

                # Add to history
                st.session_state.scraping_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'country': country,
                    'city': city,
                    'industry': industry,
                    'results_count': len(results)
                })

                st.success(f"✅ Successfully scraped {len(results)} businesses!")
            else:
                st.warning("No results found. Try adjusting your search parameters.")

            st.session_state.is_scraping = False

    # Display results
    if st.session_state.scraping_results is not None and not st.session_state.scraping_results.empty:
        st.markdown("---")
        st.header("📊 Results")

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        df = st.session_state.edited_data if st.session_state.edited_data is not None else st.session_state.scraping_results

        with col1:
            st.metric("Total Companies", len(df))

        with col2:
            phone_count = df['phone_number'].notna().sum()
            st.metric("With Phone", phone_count)

        with col3:
            website_count = df['website'].notna().sum()
            st.metric("With Website", website_count)

        with col4:
            completeness = round((phone_count + website_count) / (len(df) * 2) * 100, 1)
            st.metric("Data Completeness", f"{completeness}%")

        st.markdown("---")

        # Editable data table
        st.subheader("📝 Edit Results")
        st.markdown("You can edit the data below before downloading:")

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "company_name": st.column_config.TextColumn("Company Name", width="medium"),
                "phone_number": st.column_config.TextColumn("Phone", width="small"),
                "website": st.column_config.LinkColumn("Website", width="medium"),
                "location": st.column_config.TextColumn("Location", width="large"),
                "industry": st.column_config.TextColumn("Industry", width="small"),
                "city": st.column_config.TextColumn("City", width="small"),
                "country": st.column_config.TextColumn("Country", width="small"),
            },
            hide_index=True,
        )

        # Update edited data in session state
        st.session_state.edited_data = edited_df

        st.markdown("---")

        # Download section
        st.subheader("💾 Export Data")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            filename = st.text_input(
                "Filename",
                value=f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                help="Enter a filename for your CSV export"
            )

        with col2:
            # Convert to CSV
            csv_buffer = io.StringIO()
            edited_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )

        with col3:
            if st.button("🗑️ Clear Results", use_container_width=True):
                st.session_state.scraping_results = None
                st.session_state.edited_data = None
                st.rerun()

    # Scraping history sidebar
    if st.session_state.scraping_history:
        st.sidebar.markdown("---")
        st.sidebar.header("📜 Scraping History")

        for i, record in enumerate(reversed(st.session_state.scraping_history[-5:])):
            with st.sidebar.expander(f"🕐 {record['timestamp']}", expanded=False):
                st.text(f"Location: {record['city']}, {record['country']}")
                st.text(f"Industry: {record['industry']}")
                st.text(f"Results: {record['results_count']}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Built with ❤️ using Streamlit | Google Maps Company Scraper v1.0</p>
            <p style='font-size: 0.8em;'>⚠️ Use responsibly and comply with Google's Terms of Service</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
