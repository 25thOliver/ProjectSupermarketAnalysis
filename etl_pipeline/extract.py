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