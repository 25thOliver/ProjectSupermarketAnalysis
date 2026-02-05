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