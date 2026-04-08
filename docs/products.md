# Products API

This section describes endpoints for retrieving product data ingested from partner catalog feeds.

The Products API allows clients to:

* Retrieve all products across partners
* Filter products by multiple attributes
* Paginate results using `limit` and `offset`
* Retrieve a single product by ID

---

## GET /products

### Description

Returns product records stored from uploaded partner feeds.

Supports filtering by `partner_name`, `feed_id`, `sku`, `brand`, and `category`.

Supports offset-based pagination via `limit` and `offset` parameters.

---

### Query Parameters

| Name         | Type   | Required | Description                                                     |
|--------------|--------|----------|-----------------------------------------------------------------|
| partner_name | string | No       | Filter by partner name                                          |
| feed_id      | string | No       | Filter by feed ID                                               |
| sku          | string | No       | Filter by SKU                                                   |
| brand        | string | No       | Filter by brand                                                 |
| category     | string | No       | Filter by category                                              |
| limit        | int    | No       | Number of results to return (default: 50, max: 500)             |
| offset       | int    | No       | Number of records to skip before returning results (default: 0) |

---

### Pagination

Results can be paginated using `limit` and `offset`.

Examples:

* `GET /products?limit=10&offset=0` → first 10 products
* `GET /products?limit=10&offset=10` → next 10 products

The `count` field in the response represents the total number of matching products, not just the number returned in the current page.

---

### Example Request

```http
GET /products?partner_name=Tech Haven&limit=5&offset=0
X-API-Key: demo-secret-key
```

---

### Example Response

```json
{
  "count": 124,
  "items": [
    {
      "product_id": "PR001",
      "feed_id": "FD001",
      "partner_name": "Tech Haven",
      "sku": "EL-3001",
      "product_name": "iPhone 15 Pro",
      "description": "Apple smartphone with A17 Pro chip and titanium design",
      "brand": "Apple",
      "category": "Smartphones",
      "price": 999.0,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ]
}
```

---

### Response Fields

| Field | Type  | Description                                   |
|-------|-------|-----------------------------------------------|
| count | int   | Total number of products matching the filters |
| items | array | List of product objects for the current page  |

---

## GET /products/{product_id}

### Description

Returns a single product by its unique product ID.

---

### Path Parameters

| Name       | Type   | Required | Description                       |
|------------|--------|----------|-----------------------------------|
| product_id | string | Yes      | Unique identifier for the product |

---

### Example Request

```http
GET /products/PR001
X-API-Key: demo-secret-key
```

---

### Example Response

```json
{
  "product_id": "PR001",
  "feed_id": "FD001",
  "partner_name": "Tech Haven",
  "sku": "EL-3001",
  "product_name": "iPhone 15 Pro",
  "description": "Apple smartphone with A17 Pro chip and titanium design",
  "brand": "Apple",
  "category": "Smartphones",
  "price": 999.0,
  "currency": "USD",
  "availability": "in_stock",
  "created_at": "2026-04-08T12:00:00Z"
}
```

---

### Errors

| Status Code   | Description                                  |
|---------------|----------------------------------------------|
| 404 Not Found | Product with the specified ID does not exist |

---

## GET /products/by-feed/{feed_id}

### Description

Returns all products associated with a specific feed.

---

### Path Parameters

| Name    | Type   | Required | Description                    |
|---------|--------|----------|--------------------------------|
| feed_id | string | Yes      | Unique identifier for the feed |

---

### Example Request

```http
GET /products/by-feed/FD001
X-API-Key: demo-secret-key
```

---

### Example Response

```json
{
  "count": 10,
  "items": [
    {
      "product_id": "PR001",
      "feed_id": "FD001",
      "partner_name": "Elite Jewelry",
      "sku": "JW-1001",
      "product_name": "Diamond Stud Earrings",
      "price": 899.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ]
}
```

---

## Notes

* All endpoints require a valid `X-API-Key` header.
* Product data is sourced from uploaded partner CSV feeds.
* Not all fields are guaranteed to be populated for every product.
* Results are ordered by `created_at` in descending order by default.
