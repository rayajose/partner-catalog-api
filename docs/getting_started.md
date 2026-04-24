# Getting Started

This guide helps you quickly begin using the Partner Catalog API, including authentication, making requests, and understanding responses.

---

## Base URL

Local:

```
http://localhost:8000
```

Production:

```
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com/docs
```

---

## Authentication

All requests require an API key passed in the request header:

```
x-api-key: demo-secret-key
```

---

## Example Request

Retrieve a list of products:

```bash
curl -X GET "http://localhost:8000/products?limit=5" \
  -H "x-api-key: demo-secret-key"
```

---

## Example Response

```json
{
  "count": 10,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "ACM-001",
      "product_name": "Running Shoes",
      "description": "Lightweight running shoes designed for comfort and performance.",
      "brand": "Acme",
      "category": "Footwear",
      "price": 79.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-15T10:00:00Z"
    }
  ]
}
```

---

## Common Query Parameters

### Pagination

| Parameter | Description                                         |
|-----------|-----------------------------------------------------|
| `limit`   | Number of results to return (default: 10, max: 100) |
| `cursor`  | Cursor for retrieving the next page of results      |

### Filtering

| Parameter      | Description            |
|----------------|------------------------|
| `partner_name` | Filter by partner name |
| `feed_id`      | Filter by feed ID      |
| `brand`        | Filter by brand        |
| `category`     | Filter by category     |
| `availability` | Filter by availability |

### Sorting

| Parameter | Description                                                    |
|-----------|----------------------------------------------------------------|
| `sort_by` | Field to sort by (e.g., `price`, `created_at`, `product_name`) |
| `order`   | Sort order: `asc` or `desc`                                    |

---

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Meaning                                   |
|-------------|-------------------------------------------|
| 200         | Request successful                        |
| 400         | Bad request (invalid input)               |
| 401         | Unauthorized (missing or invalid API key) |
| 404         | Resource not found                        |
| 500         | Internal server error                     |

### Example Error Response

```json
{
  "detail": "Invalid API key"
}
```

---

## Next Steps

* Review the [Feeds](feeds.md) endpoint for uploading product feeds
* Explore [Products](products.md) for querying catalog data
* Check [Jobs](jobs.md) for tracking background processing
* Follow [Workflows](workflows.md) for end-to-end usage examples

---
