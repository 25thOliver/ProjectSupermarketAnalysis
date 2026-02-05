import pandas as pd 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_from_public_sheet(sheet_id):
    """
    Reads data from a public Google Sheet using the CSV export URL.
    Does NOT require authentication/credentials.
    """
    try:
        export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        logger.info(f"Attempting to download from public URL: {export_url}")
        
        df = pd.read_csv(export_url)
        
        if df.empty:
            logger.warning("Downloaded data is empty.")
            return pd.DataFrame()

        logger.info(f"Successfully extracted {len(df)} rows form Public Google Sheet.")
        return df

    except Exception as e:
        logger.error(f"Failed to extract from public sheet: {e}")
        raise

def extract_data(source_type='sheets', **kwargs):
    """Factory function to handle extraction."""
    # We default to public sheet if that's the requested type
    # For now, let's treat 'sheets' as public sheet extraction since we have no credentials
    if source_type.lower() == 'sheets':
        return extract_from_public_sheet(kwargs.get('sheet_id'))
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")