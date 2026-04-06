# Architecture

This document describes the high-level architecture of the Partner Catalog API, including its components, data flow, and design decisions.

---

## 🧩 System Overview

The Partner Catalog API is a layered application designed to:

* Ingest partner product feeds (CSV)
* Validate feed structure
* Track processing via jobs
* Persist data using a relational database

---

## 🏗️ Architecture Layers

```text
Client (curl / Postman / UI)
        ↓
Router Layer (FastAPI endpoints)
        ↓
Data Layer (stores.py)
        ↓
Database (SQLite)
```

---

### 1. Router Layer (`routers/`)

Handles:

* HTTP request/response processing
* Input validation (via FastAPI and Pydantic)
* Authentication (API key)
* Orchestration of business logic

**Examples:**

* `POST /feeds/upload`
* `GET /feeds/{feed_id}`
* `GET /jobs/{job_id}`

---

### 2. Data Layer (`data/stores.py`)

Responsible for:

* Database interaction (CRUD operations)
* ID generation
* Data retrieval and updates
* Mapping between database and API response formats

This layer isolates persistence logic from API logic.

---

### 3. Database Layer (`db.py`, SQLite)

Stores:

* Feed metadata
* Job metadata
* ID counters for structured identifiers

Key tables:

* `feeds`
* `jobs`
* `id_counters`

---

## 🔄 Data Flow

### Feed Upload Workflow

```text
Client
  ↓
POST /feeds/upload
  ↓
Validate file (CSV)
  ↓
Generate IDs (FDxxx, JSxxx, JVxxx)
  ↓
Persist feed (feeds table)
  ↓
Persist submission job (jobs table)
  ↓
Persist validation job (jobs table)
  ↓
Return response to client
```

---

### Feed Retrieval Workflow

```text
Client
  ↓
GET /feeds/{feed_id}
  ↓
Fetch from database
  ↓
Map DB fields → API response fields
  ↓
Return response
```

---

## 🔑 Identifier Strategy

The API uses structured identifiers for traceability:

| Prefix | Resource       | Example |
| ------ | -------------- | ------- |
| FD     | Feed           | FD001   |
| JS     | Submission Job | JS001   |
| JV     | Validation Job | JV001   |

Identifiers are generated using a database-backed counter to ensure uniqueness and persistence.

---

## 🔁 Data Mapping Strategy

The system separates internal storage format from API output format.

### Example

| Layer        | Field Name  |
| ------------ | ----------- |
| Database     | `filename`  |
| API Response | `file_name` |

This mapping is handled in the data layer to maintain:

* Consistent API naming (`snake_case`)
* Flexibility for future schema changes

---

## ⚙️ Job Model

Each feed generates two jobs:

1. **Submission Job (`JSxxx`)**

   * Tracks upload processing
   * Typically completes immediately

2. **Validation Job (`JVxxx`)**

   * Validates CSV structure
   * Determines feed readiness

Jobs provide traceability and simulate asynchronous processing.

---

## 🧠 Design Decisions

### Separation of Concerns

* Routers handle HTTP concerns
* Stores handle persistence
* Database handles storage

This improves maintainability and testability.

---

### Persistence Over In-Memory Storage

* SQLite ensures data survives application restarts
* Enables realistic system behavior

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

## 🔮 Future Enhancements

The architecture is designed to support:

* Product-level storage (parsed from CSV)
* Search and filtering endpoints
* Pagination
* Background job processing (e.g., Celery, queues)
* Cloud database integration (e.g., PostgreSQL, AWS RDS)

---

## 📂 Project Structure

```text
app/
  main.py
  db.py
  security.py
  settings.py
  data/
    stores.py
  routers/
    feeds.py
    jobs.py
  schemas/
    feeds.py
    jobs.py
    common.py
  docs/
    *.md
```

---

## 🔗 Related Documentation

* [Index](index.md)
* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Workflows](workflows.md)
* [Errors](errors.md)
