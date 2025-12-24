"""
CSV Export Module
Handles exporting scraped data to CSV files.
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict
import logging


class CSVExporter:
    """Handles exporting business data to CSV files."""

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the CSV exporter.

        Args:
            output_dir: Directory to save CSV files (default: "output")
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.logger.info(f"Created output directory: {self.output_dir}")

    def export_to_csv(self, data: List[Dict], filename: str = None) -> str:
        """
        Export business data to a CSV file.

        Args:
            data: List of dictionaries containing business information
            filename: Custom filename (optional). If not provided, generates timestamp-based name.

        Returns:
            Path to the created CSV file
        """
        if not data:
            self.logger.warning("No data to export")
            return None

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"companies_{timestamp}.csv"

        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'

        filepath = os.path.join(self.output_dir, filename)

        # Create DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to match requirements
        column_order = [
            'company_name',
            'phone_number',
            'website',
            'owner_first_name',
            'owner_last_name',
            'location',
            'industry',
            'city',
            'country'
        ]

        # Only include columns that exist in the data
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]

        # Export to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')

        self.logger.info(f"Exported {len(data)} records to {filepath}")
        print(f"\n✓ Data exported successfully to: {filepath}")
        print(f"  Total records: {len(data)}")

        return filepath

    def append_to_csv(self, data: List[Dict], filepath: str):
        """
        Append data to an existing CSV file.

        Args:
            data: List of dictionaries containing business information
            filepath: Path to existing CSV file
        """
        if not data:
            self.logger.warning("No data to append")
            return

        df_new = pd.DataFrame(data)

        # Check if file exists
        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(filepath, index=False, encoding='utf-8')
            self.logger.info(f"Appended {len(data)} records to {filepath}")
        else:
            # File doesn't exist, create new one
            self.export_to_csv(data, os.path.basename(filepath))

    def get_summary(self, filepath: str) -> Dict:
        """
        Get summary statistics from a CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            Dictionary with summary statistics
        """
        if not os.path.exists(filepath):
            self.logger.error(f"File not found: {filepath}")
            return {}

        df = pd.read_csv(filepath)

        summary = {
            'total_records': len(df),
            'records_with_phone': df['phone_number'].notna().sum(),
            'records_with_website': df['website'].notna().sum(),
            'unique_cities': df['city'].nunique() if 'city' in df.columns else 0,
            'unique_industries': df['industry'].nunique() if 'industry' in df.columns else 0
        }

        return summary
