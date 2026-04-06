# Partner Catalog API

A REST API for submitting, validating, and tracking partner product feeds.

This project demonstrates API design, data modeling, and developer-focused documentation using a realistic e-commerce ingestion workflow.

---

## 🎯 Purpose

This project demonstrates my ability to:

* Design and implement REST APIs
* Create structured, developer-focused documentation
* Model data and workflows using OpenAPI and JSON schemas
* Build a persistence-backed service (SQLite)
* Apply real-world concepts from e-commerce and partner onboarding systems

The API simulates a partner product ingestion workflow similar to systems used in large-scale retail and rewards platforms.

---

## 🚀 Quick Start

### Base URL

```
http://127.0.0.1:8000
```

### Interactive API (Swagger)

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

This API uses a header-based API key.

Include the following header in all requests:

```
X-API-Key: demo-secret-key
```

---

## 📌 Overview

The Partner Catalog API allows you to:

* Upload product feeds (CSV)
* Validate feed structure
* Track processing via jobs
* Retrieve feed metadata
* Persist feed and job data in a database

---

## 🔄 Typical Workflow

### Submit and process a feed

1. Upload a feed
   `POST /feeds/upload`

2. Track submission job
   `GET /jobs/{job_id}`

3. Track validation job
   `GET /jobs/{validation_job_id}`

4. Retrieve feed metadata
   `GET /feeds/{feed_id}`

---

## 📦 Resources

| Resource | Description                                  |
| -------- | -------------------------------------------- |
| Feed     | A partner-submitted product file (CSV)       |
| Job      | A processing task (submission or validation) |

See [Resources](resources.md) for full definitions.

---

## 📚 API Reference

* [Feeds](feeds.md)
* [Jobs](jobs.md)
* [Errors](errors.md)

---

## 🧠 Key Concepts

### Asynchronous Processing

Feed processing is modeled using jobs:

* Feed is uploaded → submission job is created
* Validation is performed → validation job is created
* Jobs track status independently of the request lifecycle

---

### Persistence

Unlike simple demo APIs, this project uses a database:

* Feed and job metadata are stored in SQLite
* Data persists across application restarts
* ID generation is managed via database-backed counters

---

### Consistent API Design

* All response fields use `snake_case`
* Resource identifiers follow a structured format:

  * `FD001` → Feed ID
  * `JS001` → Submission Job
  * `JV001` → Validation Job

---

### Error Handling

Errors follow a consistent structure:

```json
{
  "detail": "Human-readable error message"
}
```

See [Errors](errors.md) for full details.

---

## 🛠️ Technology

* FastAPI
* Python
* SQLite
* OpenAPI (Swagger)
* MkDocs

---

## 📎 Notes

* This API is designed as a portfolio project to demonstrate real-world API patterns
* CSV contents are validated but not yet persisted as product records (planned enhancement)
* Future enhancements may include:

  * Product-level storage and query endpoints
  * Pagination and filtering
  * Background job processing
