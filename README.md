# Partner Catalog API

A demo REST API for ingesting, validating, and querying product data from multiple partner feeds.

This project demonstrates API design, data modeling, and developer-focused documentation for a multi-partner catalog platform.

---

## Overview

The Partner Catalog API simulates a real-world e-commerce ingestion pipeline where external partners submit product data feeds that are processed and made available for querying.

Designed to simulate a multi-partner catalog ingestion platform similar to systems used by Shopify, Amazon Marketplace, and enterprise e-commerce platforms.

Key capabilities include:

* Feed ingestion via CSV upload
* Job-based processing and validation tracking
* Product storage and retrieval
* Filtering and pagination support
* API key-based authentication

---

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

### Flow

1. Partner uploads a product feed (`/feeds/upload`)
2. A submission job is created
3. Feed is validated via a validation job
4. Products are stored in the database
5. Products are retrieved via `/products`

---

## Authentication

All endpoints require an API key passed in the request header:

```http
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

The `/products` endpoint supports offset-based pagination:

* `limit` — number of records to return
* `offset` — number of records to skip

Example:

```
GET /products?limit=10&offset=20
```

The response includes:

* `count` — total matching records
* `items` — current page of results

---

## Sample Data

Example product categories supported:

* Jewelry
* Vinyl records
* Consumer electronics
* Craft beer

These demonstrate how the API supports multiple partner domains with a unified data model.

---

## Running the API

Start the server using:

```bash
uvicorn app.main:app --reload
```

Then access:

* Swagger UI: http://127.0.0.1:8000/docs
* OpenAPI schema: http://127.0.0.1:8000/openapi.json

---

## Future Enhancements

Potential improvements:

* Sorting (`sort_by`, `order`)
* Advanced filtering (price ranges, date filters)
* Cursor-based pagination
* Async background job processing
* Cloud deployment (AWS)

---

## Purpose

This project was built as a portfolio demonstration of:

* REST API design
* Data ingestion workflows
* Technical documentation
* Backend system modeling

---

## Author

Ray Jose
