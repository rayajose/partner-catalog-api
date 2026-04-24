# Partner Catalog API

A production-style REST API for ingesting, validating, and querying product data from multiple partner feeds.

This project demonstrates end-to-end API development, including data ingestion workflows, cloud deployment on AWS (ECS Fargate + RDS), and developer-focused documentation.

---
## Purpose

This project was built as a portfolio demonstration of:

* REST API design
* Data ingestion workflows
* Cloud deployment (AWS ECS, RDS, ALB)
* Technical documentation
* Backend system modeling
---

## Tech Stack

- FastAPI (Python)
- PostgreSQL (Amazon RDS)
- Docker
- Amazon ECS (Fargate)
- Application Load Balancer (ALB)
- Amazon ECR
- MkDocs (documentation)

## Live API

Swagger UI:
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs

> Note: The API may be temporarily offline outside of demonstration periods to control cloud costs.

### Example Request

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/products?limit=5"
```
---

## Overview

The Partner Catalog API simulates a real-world e-commerce ingestion pipeline where external partners submit product data feeds that are processed and made available for querying.

Designed to reflect multi-partner catalog ingestion systems used by platforms like Amazon Marketplace and enterprise e-commerce solutions.

### Key capabilities

* Feed ingestion via CSV upload
* Job-based processing and validation tracking
* Product storage and retrieval
* Filtering, sorting, and pagination
* API key-based authentication

---

## API Documentation (Live)

The API is deployed to AWS and accessible via Swagger UI.

### Swagger Overview
![swagger-overview.png](docs/screenshots/swagger-overview.png)

---

### Products Endpoint
![swagger-products-endpoint.png](docs/screenshots/swagger-products-endpoint.png)

### Live API Response



## Architecture

The API is built using **FastAPI** and follows a modular structure:

```
app/
├── main.py
├── routers/
│   ├── feeds.py
│   ├── jobs.py
│   └── products.py
├── schemas/
│   ├── feeds.py
│   ├── jobs.py
│   └── products.py
├── db.py
```

### Ingestion Flow

1. Partner uploads a product feed (`/feeds/upload`)
2. A submission job is created
3. Feed is validated via a validation job
4. Products are stored in the database
5. Products are retrieved via `/products`

---

## Deployment (AWS)

This API is deployed using a containerized cloud architecture:

* FastAPI (Docker)
* Amazon ECS (Fargate)
* Amazon RDS (PostgreSQL)
* Application Load Balancer (ALB)
* Amazon ECR

Full deployment details:
[docs/deployment.md](docs/deployment.md)

---

## Authentication

All endpoints require an API key passed in the request header:

```
X-API-Key: demo-secret-key
```

Requests without a valid API key will return:

```json
{
  "detail": "Unauthorized"
}
```

---

## Endpoints

### Feeds

* `POST /feeds/upload` — Upload a product feed
* `GET /feeds` — List feeds
* `GET /feeds/{feed_id}` — Retrieve a feed

### Jobs

* `GET /jobs/{job_id}` — Retrieve job status

### Products

* `GET /products` — List and filter products
* `GET /products/{product_id}` — Retrieve a single product
* `GET /products/by-feed/{feed_id}` — Retrieve products by feed

---

## Pagination

The `/products` endpoint uses **cursor-based pagination**.

* `limit` — number of records to return
* `cursor` — last seen `product_id`

Example:

```
GET /products?limit=10&cursor=PR00010
```

Response includes:

* `count` — number of items returned
* `items` — current page of results
* `next_cursor` — pointer for next page (if more data exists)

---

## Filtering & Sorting

Supported filters:

* `partner_name`
* `feed_id`
* `sku`
* `brand`
* `category`
* `availability`

Sorting:

* `sort_by`: `created_at`, `price`, `product_name`, `brand`, `category`
* `order`: `asc`, `desc`

---

## Sample Data

Example product categories supported:

* Jewelry
* Vinyl records
* Consumer electronics
* Craft beer
* Running shoes

These demonstrate support for multiple partner domains within a unified data model.

---

## Run Locally

Follow these steps to run the API locally using Docker and PostgreSQL.

### Prerequisites

* Python 3.11+
* Docker Desktop
* Git

---

### 1. Clone the repository

```bash
git clone https://github.com/rayajose/partner-catalog-api.git
cd partner-catalog-api
```

---

### 2. (Optional) Run with Python (virtual environment)

```bash
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

### 3. Run with Docker (recommended)

Build the image:

```bash
docker build -t partner-catalog-api .
```

Run the container:

```bash
docker run -p 8000:8000 ^
  -e DB_TYPE=postgres ^
  -e DB_HOST=host.docker.internal ^
  -e DB_PORT=5432 ^
  -e DB_NAME=partner_catalog ^
  -e DB_USER=postgres ^
  -e DB_PASSWORD=your_password ^
  partner-catalog-api
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Required environment variables

| Variable    | Description              |
|-------------|--------------------------|
| DB_TYPE     | Database type (postgres) |
| DB_HOST     | Database host            |
| DB_PORT     | Database port            |
| DB_NAME     | Database name            |
| DB_USER     | Database user            |
| DB_PASSWORD | Database password        |

---

### 5. API Authentication

All requests require an API key passed in the header:

```bash
x-api-key: demo-secret-key
```

---

### Notes

* For local Docker runs, `host.docker.internal` is used to connect to a database running on your host machine
* For AWS deployment, `DB_HOST` is set to the RDS endpoint
* Swagger UI is available at `/docs`


## Author

Ray Jose
