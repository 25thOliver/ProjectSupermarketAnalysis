import pandas as pd 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_from_sheet(sheet_id, credentials_path):
    # Read data from Google sheet using gspread.
    try:
        logger.info(f"Connecting to Google sheet ID: {sheet_id}")

        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found at: {credentials_path}")

        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Authenticate
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)

        # Try open the sheet by key
        sheet = client.open_by_key(sheet_id).sheet1 # This assumes data is in the first sheet

        logger.info("Successfully connected to Google sheet. Downloading data...")
        data = sheet.get_all_records()

        if not data:
            logger.warning("Sheet appears to be empty!")
            return pd.DataFrame()

        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        logger.info(f"Successfully extracted {len(df)} rows from Google Sheet")
        return df

    except Exception as e:
        logger.error(f"Failed to extract data from Google Sheet: {e}")
        raise
    
def extract_data(source_type='sheets', **kwargs):
    # Factory function to handle extraction
    if source_type.lower() == 'sheets':
        return extract_from_sheet(
            kwargs.get('sheet_id'),
            kwargs.get('credentials_path')
        )
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")