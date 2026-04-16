# Partner Catalog API

A REST API for submitting, validating, and querying partner product feeds.

This project demonstrates API design, data modeling, cloud deployment, and developer-focused documentation using a realistic e-commerce ingestion workflow.

---

## Purpose

This project demonstrates my ability to:

* Design and implement REST APIs
* Create structured, developer-focused documentation
* Model data and workflows using OpenAPI and JSON schemas
* Build a persistence-backed service (SQLite locally, PostgreSQL in production)
* Deploy and troubleshoot a cloud-based application (AWS ECS, RDS, ALB)

The API simulates a partner product ingestion workflow similar to systems used in large-scale retail and rewards platforms.

---

## Quick Start

### Base URL (Local)

```text id="idx1"
http://127.0.0.1:8000
```

### Interactive API (Swagger)

```text id="idx2"
http://127.0.0.1:8000/docs
```

---

## Live API

> Note: The live deployment may be temporarily offline to control cloud costs.

```text id="idx3"
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs
```

---

## Authentication

This API uses a header-based API key.

Include the following header in all requests:

```text id="idx4"
X-API-Key: demo-secret-key
```

---

## Overview

The Partner Catalog API allows you to:

* Upload product feeds (CSV)
* Validate feed structure and content
* Track processing via jobs
* Retrieve feed metadata
* Store and query product data
* Filter, sort, and paginate results

---

## Typical Workflow

### Submit and process a feed

1. Upload a feed
   `POST /feeds/upload`

2. Track submission job
   `GET /jobs/{job_id}`

3. Track validation job
   `GET /jobs/{validation_job_id}`

4. Retrieve feed metadata
   `GET /feeds/{feed_id}`

5. Query products
   `GET /products`

---

## Resources

| Resource | Description                                     |
| -------- | ----------------------------------------------- |
| Feed     | A partner-submitted product file (CSV)          |
| Job      | A processing task (submission or validation)    |
| Product  | A normalized product record derived from a feed |

See [Resources](resources.md) for full definitions.

---

## API Reference

* [Feeds](feeds.md)
* [Jobs](jobs.md)
* [Products](products.md)
* [Errors](errors.md)

---

## Key Concepts

### Job-Based Processing

Feed processing is modeled using jobs:

* Feed upload → submission job created
* Validation → validation job created
* Jobs track processing independently of request lifecycle

---

### Persistence

This project uses a relational database:

* SQLite for local development
* PostgreSQL (AWS RDS) in production
* Data persists across application restarts
* ID generation is managed via database-backed counters

---

### Cursor-Based Pagination

Product queries use cursor-based pagination:

* More efficient than offset-based pagination
* Scales better for large datasets
* Uses `product_id` as the cursor

---

### Consistent API Design

* All response fields use `snake_case`
* Resource identifiers follow a structured format:

  * `FD00001` → Feed ID
  * `JS00001` → Submission Job
  * `JV00001` → Validation Job
  * `PR00001` → Product ID

---

### Error Handling

Errors follow a consistent structure:

```json id="idx5"
{
  "detail": "Human-readable error message"
}
```

See [Errors](errors.md) for full details.

---

## Technology

* FastAPI
* Python
* PostgreSQL (RDS) / SQLite (local)
* Docker
* AWS ECS (Fargate)
* Application Load Balancer
* Amazon ECR
* OpenAPI (Swagger)
* Markdown-based documentation

---

## Notes

* This API is designed as a portfolio project to demonstrate real-world API and cloud deployment patterns
* Product data is parsed from CSV feeds and stored for querying
* Deployment is containerized and cloud-hosted

### Potential Enhancements

* Background job processing (queues/workers)
* Advanced filtering (ranges, search)
* Event-driven ingestion pipelines
* Horizontal scaling (multiple ECS tasks)
* Infrastructure as Code (CloudFormation / Terraform)
