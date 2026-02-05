import pandas as pd
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

logger = logging.getLogger(__name__)

def load_to_mongo(df, mongo_uri, db_name, collection_name="transactions"):
    # Load the transformed data into MongoDB
    try:
        logger.info("Connecting to MongoDB...")
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        logger.info("Connection successful.")

        # Convert DataFrame to a list of dictionaries (records)
        records = df.to_dict("records")

        logger.info(f"Loading {len(records)} documents into MongoDB collection '{collection_name}'...")

        # Bulk insert (or upsert logic if you prefer)
        collection.drop()
        logger.info("Dropped existing collection for clean load.")

        if records:
            collection.insert_many(records)

        logger.info("Data loaded successfully to MongoDB")

        # Create an index on 'id' for faster lookups
        collection.create_index("id", unique=True)
        logger.info("index created on 'id'.")
    
    except PyMongoError as e:
        logger.error(f"MongoDB Error loading data: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading to MongoDB: {e}")
        raise