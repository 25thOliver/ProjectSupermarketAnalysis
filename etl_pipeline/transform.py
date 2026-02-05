import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_data(df):
    # Cleans and transforms the extracted data.
    try:
        logger.info("Starting data transformation...")
        
        # 1. Select required columns
        required_columns = [
            "id", "quantity", "product_name", 
            "total_amount", "payment_method", "customer_type"
        ]

        # Check if all columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        df_transformed = df[required_columns].copy()

        # 2. Basic Cleaning
        # Remove duplicates
        initial_count = len(df_transformed)
        df_transformed.drop_duplicates(subset=['id'], inplace=True)
        final_count = len(df_transformed)

        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} duplicate rows based on the 'id'.")

        # Handle missing values 
        df_transformed.dropna(subset=['id'], inplace=True)

        logger.info("Data transformation complete.")
        return df_transformed

    except Exception as e:
        logger.error(f"Error transforming data: {e}")
        raise