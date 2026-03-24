# Partner Catalog API

A REST API for submitting, validating, and tracking partner product feeds.

This project demonstrates API design, schema modeling, and developer-focused documentation.

---

## 🎯 Purpose

This project demonstrates my ability to:

- Design and document REST APIs  
- Create structured, developer-focused documentation  
- Model data and workflows using OpenAPI and JSON schemas  
- Apply real-world concepts from e-commerce and partner onboarding systems  

The API simulates a partner product ingestion workflow, similar to systems used in large-scale retail and rewards platforms.

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

## 📌 Overview

The Partner Catalog API allows you to:

* Submit product feeds from partners
* Validate feeds asynchronously
* Track processing jobs and status
* Retrieve feed data

---

## 🔄 Typical Workflow

### Submit and validate a feed

1. Create a feed
   `POST /feeds`

2. Start validation
   `POST /feeds/{feed_id}/validate`

3. Check job status
   `GET /jobs/{job_id}`

---

## 📦 Resources

| Resource | Description                             |
| -------- | --------------------------------------- |
| Feed     | A partner-submitted product file        |
| Job      | A background process such as validation |

See [Resources](resources.md) for full definitions.

---

## 📚 API Reference

* [Feeds](feeds.md)
* [Jobs](jobs.md)
* [Errors](errors.md)

---

## 🧠 Key Concepts

### Asynchronous Processing

Feed validation runs as a background job:

* A feed is created → job is queued
* Validation starts → job is running
* Job completes → status is updated

---

### Pagination

List endpoints support:

* `limit` — max results
* `offset` — starting position

---

### Error Handling

All errors follow a standard format:

```json
{
  "error_code": "STRING_CODE",
  "message": "Human-readable summary",
  "details": {}
}
```

See [Errors](errors.md) for details.

---

## 🛠️ Technology

* FastAPI
* Python
* OpenAPI (Swagger)
* MkDocs

---

## 📎 Notes

This API uses in-memory storage for demonstration purposes.
Data is reset when the application restarts.
