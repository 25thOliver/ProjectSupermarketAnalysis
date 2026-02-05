import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def load_to_postgres(df, db_url, table_name="transactions"):
    # Load the transformed data into PostgreSQL
    try:
        logger.info("Connecting to PostgreSQL")
        # Create SQLAlchemy engine
        engine = create_engine(db_url)

        # Verify connection
        with engine.connect() as connection:
            logger.info("Connection successful.")
            logger.info(f"Loading {len(df)} rows into PostgreSQL table '{table_name}'...")

            # Write data to SQL
            # if_exists='replace': Drops the table if it exists and creates a new one
            # This ensures we have a fresh copy of the clean data.
            # if_exists='append': Would add to existing data (good for incremental).
            df.to_sql(table_name, engine, if_exists='replace', index=False)

            logger.info("Data loaded successfully to PostgreSQL.")

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy Error loading data to PostgreSQL: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading to PostgreSQL: {e}")
        raise    