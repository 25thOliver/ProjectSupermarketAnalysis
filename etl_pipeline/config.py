import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    # Database Config
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "supermarket")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")
    MONGO_DB = os.getenv("MONGO_DB", "supermarket")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", "27017")

    # App Config
    DATA_SOURCE_TYPE = os.getenv("DATA_SOURCE_TYPE", "sheets")

    # Google Sheets Config
    # The sheet ID extracted from the URL
    https://docs.google.com/spreadsheets/d/1CHSfRQTla3Kkang7E_PptCKc6WYMIlzwDoe_hgMMajE/edit?usp=sharing
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1CHSfRQTla3Kkang7E_PptCKc6WYMIlzwDoe_hgMMajE")
    GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

    # Construct DB URLs
    POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
