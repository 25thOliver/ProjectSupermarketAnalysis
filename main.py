from etl_pipeline.config import Config
from etl_pipeline.extract import extract_data
import sys
import logging

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def main():
    logging.info("ETL Application pipeline initialized.")
    
    # 1. Extract
    try:
        if Config.DATA_SOURCE_TYPE == "sheets":
            logging.info(f"Starting extraction from Google Sheets (ID: {Config.GOOGLE_SHEET_ID})")
            
            # Extract data
            data = extract_data(
                source_type="sheets",
                sheet_id=Config.GOOGLE_SHEET_ID,
                credentials_path=Config.GOOGLE_SHEETS_CREDENTIALS
            )
        else:
            logging.error(f"Unknown data source: {Config.DATA_SOURCE_TYPE}")
            return

        logging.info("\nExtraction Sample...")
        print(df.head())
        logging.info(f"\nTotal rows extracted: {len(df)}")

    except Exception as e:
        logging.critical(f"ETL failed: {e}")

if __name__ == "__main__":
    main()