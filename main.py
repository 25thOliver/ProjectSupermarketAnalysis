from etl_pipeline.config import Config
from etl_pipeline.extract import extract_data
from etl_pipeline.transform import transform_data
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
                sheet_id=Config.GOOGLE_SHEET_ID
            )
        else:
            logging.error(f"Unknown data source: {Config.DATA_SOURCE_TYPE}")
            return

        logging.info(f"Extracted {len(data)} rows.")


        # 2. Transform
        logging.info("Step 2: Transform")
        transformed_data = transform_data(data)

        logging.info("\nTransformation Sample...")
        print(transformed_data.head())
        logging.info(f"Transformed Data Shape: {transformed_data.shape}")    
        
    except Exception as e:
        logging.critical(f"ETL failed: {e}")

if __name__ == "__main__":
    main()