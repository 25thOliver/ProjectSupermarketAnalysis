# Architecture Decision Record

## 001. Dual Database Strategy: PostgreSQL and MongoDB

### Status
Accepted

### Context
The Supermarket ETL project requires processing transaction data from a source system(Google Sheets) and making it available for downstream consumption. We needed to decided on a storage startegy to support both:
1. **Structured Reporting**: Financial analysis, revenue aggregation, and strict schema enforcement.
2. **Flexible Analytics**: Rapid prototyping, storing raw/semi-structured attributes, and handling potential drift in the future.

### Decision 
I decided to implement a **Dual Database Strategy**, loading transformed data into both **PostgreSQL**  (Relational) and **MongoDB** (NoSQL) simultaneously.

### Consequences

#### PostgreSQL (Relational Transactional)
* **Pros**:
    * **Strong Consistency (ACID)**: Essential for financial data (e.g., `total_amount`).
    * **SQL Support**: Allows for complex analytical queries (joins, aggregation) familiar to business analysts.
    * **Scema Enforcement**: Prevents bad data (e.g., text in a price column) from entering a warehouse.

* **Cons**:
    * Rigid schema requires migration scripts for every change in upstream data structure.

#### MongoDB (Document Store)
* **Pros**:
    * **Schema Flexibility**: Can ingest new fields from the source without immediate code changes.
    * **JSON-native**: Maps 1:1 with modern application APIs.
    * **Scalability**: easier to scale horizontally for massive datasets in the future.

* **Cons**:
    * Weaker consistency guarantees compared to Postgres.
    * Complex joins are more difficult to perform than in SQL.

### Technical Implementation
* **Orchestration**: A Python script acts as the controller, ensuring data flows to both systems in the same run.
* **Library Choice**:
    * `Pandas` for data manipulation and cleaning.
    * `SQLAlchemy` (ORM) was chosen for Postgres to abstract SQL syntax and provide security against injection.
    * `PyMongo` was chosen for MongoDB for its lightweight and direct driver support.

### Future Considerations
* If data volume grows > 10TB, we might separate these loads into asynchronous queues (e.g., using RabbitMQ or Kafka) so that  a failure in Postgres doesn't block the load to Mongo.

---

## 002. Python as the Core Language

### Status
Accepted

### Context
I needed a programming language to handle extraction, transformation, and loading (ETL) logic. The language needed to support:
1. Robust libraries for data amanipulation.
2. Easy connectivity to various APIs (Google Sheets) and Databases.
3. Readability for future maintenance.

### Decision 
I chose **Python 3.9**.

### Consequences
* **Pros**:
    * **Ecosystem**: Access to `pandas` (industry standard for data), `gspread` (Sheets API), and `SQLAlchemy`.
    * **Development Speed**: Python's simple syntax allows for rapid prototyping of ETL scripts.
    * **Community**: Vast support for any data-related issue I might encounter.

* **Cons**:
    * Slower execution speed compared to compiled languages like Go or Rust (though negligible for our dataset size).

---

## 003. Docker Containerization

### Status 
Accepted

### Context
Historically, setting up ETL pipelines involves complex environment configuration (installing specific DB versions, Python dependencies, system libraries), leading to "it works on my machine" issues.

### Decision
I chose **Docker** and **Docker Compose** to containerize the entire stack.

### Consequences
* **Pros**:
    * **Reproducibility**: The exeact environment is defined in code (`Dockerfile`, `docker-compose.yml`).
    * **Isolation**: The database services run in their own sandboxes, preventing conflicts with local software.
    * **Onboarding**: New developers only need to run `docker compose up` to start working.

* **Cons**:
    * Adds overhead to the development process (rebuilding images).
    * Requires Docker to be installed on the host machine and knowledge to debug its issues.

---

## 004. Modular Pipeline Design

### Status 
Accepted

### Context
ETL scripts often grow into single, monolithic files (`script.py`) that are hard to debug and test. I needed a structure that promotes separation of concerns and makes the pipeline easier to maintain and scale in the future.

### Decision 
I implemented a **Modular Design** separating concerns into distinct files: 
- `config.py`: Manages configuration and environment variables.
- `extract.py`: Handles data extraction from the source.
- `transform.py`: Performs data cleaning and transformation.
- `load_postgres.py`: Loads data into PostgreSQL.
- `load_mongo.py`: Loads data into MongoDB.
- `main.py`: Orchestrates the ETL pipeline.

### Consequences
* **Pros**:
    * **Testability**: We can test the `transform` logic independently of the database connection.
    * **Maintainability**: A change in the "Extract" logic (e.g. switching from Google Sheets to a CSV) doesn't break the "Load" logic.
    * **Scalability**: We can easily add a new "Load" step (e.g. to Snowflake) without modifying the rest of the pipeline.
    * **Readability**: The `main.py` clearly shows high-level flow of data.

* **Cons**:
    * Slightly more boilerplate code (imports, shared config) compared to a single script.