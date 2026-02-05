# Supermarket ETL Pipeline

## Project Overview
This project is an automated Data Engineering pipeline designed to process supermarket transaction data. It simulates a real-world scenario where data is:
1. **Extracted** from a public Google Sheet (representing raw sales logs).
2. **Transformed** using Python (cleaning, filtering, and validation).
3. **Loaded** into two distinct databases for different use cases:
    * **PostgreSQL**: A relational database, ideal for structured reporting and financial integrity.
    * **MongoDB**: A NoSQL document store, ideal for flexible analytics and rapid application development.

The entire system is containerized using **Docker**, ensuring that it works identically on any machine without complex installation steps.

---

## Architecture
**Flow:** `Google Sheets (Source)` -> `Python Script(Container)` -> `PostgreSQL` & `MongoDB`

1. **Extraction Layer**: Connects to the data source (google Sheets) and downloads raw transaction history.
2. **Transformation Layer** Uses `pandas` to:
    * Filter for critical columns (`id`, `quantity`, `product_name`, `total_amount`, `payment_method`, `customer_type`) 
    * Remove duplicates transaction IDs to ensure data integrity.
    * Handle missing or corrupt data.
3. **Loading Layer**: Loads the transformed data into two distinct databases:
    * **PostgreSQL**: Uses `SQLAlchemy` to insert structured records into the `transactions` table.
    * **MongoDB**: Uses `PyMongo` to insert JSON-like documents into the `transactions` collection.

---

## Getting Started

### Prerequisites
*   [Docker](https://www.docker.com/) installed on your machine.
*   [Git](https://git-scm.com/) (optional, for cloning).

### 1. Setup Environment
Create a `.env` file in the root directory to store configuration.

**Essential Variables**
```ini
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=supermarket
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password
DATA_SOURCE_TYPE=sheets
GOOGLE_SHEET_ID=1CHSfRQTla3Kkang7E_PptCKc6WYMIlzwDoe_hgMMajE
```

### 2. Launch Infrastructure
Start the database containers and the appliaction environment using Docker Compose:
```bash
docker compose up -d --build
```
*This command may take a few minutes the first time as it downloads the necessary*

### 3. Run the ETL Job
Once the containers are running, execute the pipeline manually:
```bash
docker compose exec etl-app python main.py
```
**Success Output**: You should see logs indicating successful extraction, transformation, and loading messages:
```
"INFO:etl_pipeline.load_postgres:Data loaded successfully to PostgreSQL. INFO:etl_pipeline.load_mongo:Data loaded successfully to MongoDB"
```

## Technical Details
**Folder Structure**
```
project_supermarket/
├── etl_pipeline/           # Source code for the pipeline
│   ├── __init__.py
│   ├── config.py           # Configuration loader
│   ├── extract.py          # Data extraction logic
│   ├── transform.py        # Data cleaning logic
│   ├── load_postgres.py    # PostgreSQL interface
│   └── load_mongo.py       # MongoDB interface
├── main.py                 # Entry point of the application
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Python environment definition
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
Technology Stack
- Language: Python 3.9
- Data Processing: Pandas
- Databases: PostgreSQL 15, MongoDB 6
- Containerization: Docker & Docker Compose
- Libraries: `gspread`, `SQLAlchemy`, `psycopg2`, `pymongo`

---