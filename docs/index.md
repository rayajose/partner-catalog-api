# Partner Catalog API

A demo REST API that simulates real-world partner product ingestion workflows, including feed upload, validation, and product retrieval.

---

## What This Project Demonstrates

- API design for data ingestion workflows
- Developer-focused documentation (reference + workflows)
- Schema modeling and validation
- Pagination, filtering, and sorting
- Cloud deployment architecture (AWS ECS + RDS)

---

## Key Features

- Upload partner product feeds (CSV)
- Validate and process feeds asynchronously
- Query product catalog with filtering and pagination
- Track processing jobs

---

## Explore the API

- [Getting Started](getting_started.md)
- [Feeds](feeds.md)
- [Products](products.md)
- [Jobs](jobs.md)
- [Workflows](workflows.md)
- [About This Project](about.md)

---

## Architecture

- FastAPI (Python)
- PostgreSQL (RDS)
- Docker
- AWS ECS (Fargate)

---

## Live API

Interactive API (Swagger UI):

[http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs](http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs)

---

## Source Code

[https://github.com/rayajose/partner-catalog-api](https://github.com/rayajose/partner-catalog-api)