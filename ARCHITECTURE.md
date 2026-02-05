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
    * **Strong Consistency**: Essential for financial data (e.g., `total_amount`).
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

