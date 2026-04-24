# Architecture

This document describes the high-level architecture of the Partner Catalog API, including its components, data flow, and design decisions.

---

## System Overview

The Partner Catalog API is a layered application designed to:

* Ingest partner product feeds (CSV)
* Validate feed structure and content
* Track processing via jobs
* Persist data using a relational database
* Expose product data via queryable endpoints

---

## Architecture Layers

```text
Client (curl / Postman / Swagger UI)
        ↓
Router Layer (FastAPI endpoints)
        ↓
Application / Data Access Layer (db.py)
        ↓
Database (PostgreSQL / SQLite for local)
```

---

### 1. Router Layer (`routers/`)

Handles:

* HTTP request/response processing
* Input validation (FastAPI + Pydantic)
* Authentication (API key)
* Orchestration of application logic

**Examples:**

* `POST /feeds/upload`
* `GET /feeds/{feed_id}`
* `GET /jobs/{job_id}`
* `GET /products`

---

### 2. Application / Data Access Layer (`db.py`)

Responsible for:

* Database connections (SQLite locally, PostgreSQL in production)
* CRUD operations
* ID generation
* Query filtering, sorting, and pagination
* Mapping database records to API response models

This layer isolates persistence logic from API routing logic.

---

### 3. Database Layer (`db.py`, PostgreSQL / SQLite)

Stores:

* Feed metadata
* Job metadata
* Product data
* ID counters for structured identifiers

Key tables:

* `feeds`
* `jobs`
* `products`
* `id_counters`

---

## Data Flow

### Feed Upload Workflow

```text
Client
  ↓
POST /feeds/upload
  ↓
Validate file (CSV structure + content)
  ↓
Generate IDs (FDxxxxx, JSxxxxx, JVxxxxx)
  ↓
Persist feed (feeds table)
  ↓
Persist submission job (jobs table)
  ↓
Persist validation job (jobs table)
  ↓
Parse and store products (products table)
  ↓
Return response to client
```

---

### Product Query Workflow

```text
Client
  ↓
GET /products
  ↓
Apply filters, sorting, pagination
  ↓
Query database
  ↓
Map DB fields → API response schema
  ↓
Return response (items + next_cursor)
```

---

## Identifier Strategy

The API uses structured identifiers for traceability:

| Prefix | Resource       | Example |
|--------|----------------|---------|
| FD     | Feed           | FD00001 |
| JS     | Submission Job | JS00001 |
| JV     | Validation Job | JV00001 |
| PR     | Product        | PR00001 |

Identifiers are generated using a database-backed counter to ensure uniqueness and persistence.

---

## Data Mapping Strategy

The system separates internal storage format from API output format.

### Example

| Layer        | Field Name  |
|--------------|-------------|
| Database     | `filename`  |
| API Response | `file_name` |

This mapping is handled in the data access layer to maintain:

* Consistent API naming (`snake_case`)
* Flexibility for future schema changes
* Decoupling of storage and presentation models

---

## Job Model

Each feed generates two jobs:

### 1. Submission Job (`JSxxxxx`)

* Tracks upload processing
* Typically completes immediately

### 2. Validation Job (`JVxxxxx`)

* Validates CSV structure and content
* Determines feed readiness

Jobs provide traceability and simulate asynchronous processing.

---

## Design Decisions

### Separation of Concerns

* Routers handle HTTP concerns
* Data layer handles persistence and querying
* Database handles storage

This improves maintainability and testability.

---

### Relational Persistence

* SQLite used for local development
* PostgreSQL used in production (AWS RDS)
* Enables realistic, production-like behavior

---

### Cursor-Based Pagination

* Uses `product_id` as cursor
* Avoids performance issues of offset pagination
* Scales better for large datasets

---

### Synchronous Execution with Asynchronous Model

* Jobs execute immediately
* Modeled as asynchronous for future extensibility (e.g., background workers)

---

### Consistent API Design

* All fields use `snake_case`
* Predictable resource naming
* Structured identifiers improve readability and debugging

---

### Cloud-Native Deployment

* Containerized application (Docker)
* Deployed to ECS Fargate
* Database hosted on RDS
* Exposed via Application Load Balancer

---

## Future Enhancements

The architecture is designed to support:

* Full async job processing (queues, workers)
* Advanced filtering (ranges, full-text search)
* Event-driven ingestion pipelines
* Horizontal scaling (multiple ECS tasks)
* Read replicas for database scaling
* Infrastructure as Code (CloudFormation / Terraform)

---

## Project Structure

```text
app/
  main.py
  db.py
  security.py
  settings.py
  routers/
    feeds.py
    jobs.py
    products.py
  schemas/
    feeds.py
    jobs.py
    products.py
    common.py
  docs/
    *.md
```

---

## Related Documentation

* [Index](index.md)
* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Products API](products.md)
* [Workflows](workflows.md)
* [Errors](errors.md)
* For deployment evidence, see [Screenshots](screenshots.md).
