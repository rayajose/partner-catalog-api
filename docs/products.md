# Products API

This section describes endpoints for retrieving product data ingested from partner catalog feeds.

The Products API allows clients to:

* Retrieve all products across partners
* Filter products by multiple attributes
* Sort results by supported fields
* Paginate results using `limit` and `cursor`
* Retrieve a single product by ID

---

## GET /products

### Description

Returns product records stored from uploaded partner feeds.

Supports filtering, sorting, and cursor-based pagination.

---

### Query Parameters

| Name         | Type   | Required | Description                                                                   |
|--------------|--------|----------|-------------------------------------------------------------------------------|
| partner_name | string | No       | Filter by partner name                                                        |
| feed_id      | string | No       | Filter by feed ID                                                             |
| sku          | string | No       | Filter by SKU                                                                 |
| brand        | string | No       | Filter by brand                                                               |
| category     | string | No       | Filter by category                                                            |
| availability | string | No       | Filter by availability                                                        |
| limit        | int    | No       | Number of results to return (default: 10, max: 100)                           |
| cursor       | string | No       | Cursor for pagination. Use the `next_cursor` value from the previous response |
| sort_by      | string | No       | Field to sort by (created_at, price, product_name, brand, category)           |
| order        | string | No       | Sort direction (`asc`, `desc`, default: `desc`)                               |

---

### Sorting

Results can be sorted using `sort_by` and `order`.

Supported fields:

* `created_at`
* `price`
* `product_name`
* `brand`
* `category`

Examples:

```http id="p1q2r3"
GET /products?sort_by=price&order=asc
```

```http id="s4t5u6"
GET /products?sort_by=product_name&order=asc
```

---

### Pagination

Results are paginated using `limit` and `cursor`.

* The cursor is based on `product_id`
* The API returns a `next_cursor` when more results are available
* To retrieve the next page, pass the returned cursor in the next request

Examples:

```http id="v7w8x9"
GET /products?limit=5
```

```http id="y1z2a3"
GET /products?limit=5&cursor=PR00010
```

Response behavior:

* `count` = number of items returned in the current page
* `next_cursor` = present only when more results exist

---

### Example Request

```http id="b4c5d6"
GET /products?partner_name=Tech Haven&limit=5
X-API-Key: demo-secret-key
```

---

### Example Response

```json id="e7f8g9"
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
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
  ],
  "next_cursor": "PR00005"
}
```

---

### Response Fields

| Field       | Type   | Description                                  |
|-------------|--------|----------------------------------------------|
| count       | int    | Number of items returned in the current page |
| items       | array  | List of product objects                      |
| next_cursor | string | Cursor for next page (if more results exist) |

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

```http id="h1i2j3"
GET /products/PR00001
X-API-Key: demo-secret-key
```

---

### Example Response

```json id="k4l5m6"
{
  "product_id": "PR00001",
  "feed_id": "FD00001",
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

### Error Responses

#### 404 Not Found

```json
{
  "detail": "Product PR99999 not found."
}
```

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
GET /products/by-feed/FD00001
X-API-Key: demo-secret-key
```

---

### Example Response

```json
{
  "count": 10,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
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

* All endpoints require a valid `X-API-Key` header
* Product data is sourced from uploaded partner CSV feeds
* Not all fields are guaranteed to be populated for every product
* Results are ordered by `created_at` in descending order by default
* Cursor-based pagination is used for efficient data retrieval at scale
