# Feeds API

Feeds represent partner-submitted product data files. A feed moves through the lifecycle:

`uploaded → validating → validated → failed`

---

## POST /feeds

Submits a partner product feed and creates an associated processing job.

### Request Body

```json
{
  "partner_name": "Acme Corp",
  "file_name": "products.csv",
  "submitted_by": "user@example.com",
  "notes": "Initial upload"
}
```

### Fields

* `partner_name` *(string, required)* — Name of the submitting partner
* `file_name` *(string, required)* — Name of the uploaded file
* `submitted_by` *(string, required, email)* — Email address of the submitter
* `notes` *(string, optional)* — Additional context or comments

---

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/feeds" \
  -H "X-API-Key: demo-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "Acme Corp",
    "file_name": "products.csv",
    "submitted_by": "user@example.com",
    "notes": "Initial upload"
  }'
```

---

### Example Response

```json
{
  "feed_id": "FD-1",
  "status": "uploaded",
  "job_id": "SJ-1"
}
```

---

### Errors

| Status | Description      |
|--------|------------------|
| 401    | Missing API key  |
| 403    | Invalid API key  |
| 422    | Validation error |

### Example Validation Error

If `submitted_by` is not a valid email address, FastAPI returns a validation error response.

```json
{
  "detail": [
    {
      "loc": ["body", "submitted_by"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```
---

## GET /feeds

Returns a paginated list of feeds with optional filtering by status.

### Query Parameters

* `status` *(string, optional)* — Filter by feed status
* `limit` *(integer, optional, default: 10)* — Maximum number of items
* `offset` *(integer, optional, default: 0)* — Number of items to skip

---

### Example Request

```bash
curl "http://127.0.0.1:8000/feeds?status=uploaded&limit=2&offset=0" \
  -H "X-API-Key: demo-secret-key"
```

---

### Example Response

```json
{
  "items": [
    {
      "feed_id": "FD-1",
      "partner_name": "Acme Corp",
      "file_name": "products.csv",
      "status": "uploaded"
    }
  ],
  "total": 1,
  "limit": 2,
  "offset": 0
}
```

---

### Response Fields

* `items` *(array)* — List of feed objects
* `total` *(integer)* — Total number of matching feeds
* `limit` *(integer)* — Maximum number returned
* `offset` *(integer)* — Number skipped

---

### Errors

| Status | Description      |
|--------|------------------|
| 401    | Missing API key  |
| 403    | Invalid API key  |
| 422    | Validation error |

### Example Validation Error

```json
{
  "detail": [
    {
      "loc": ["query", "offset"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```
---

## GET /feeds/{feed_id}

Retrieves details for a specific feed.

### Path Parameters

* `feed_id` *(string, required)* — Unique identifier for the feed

---

### Example Request

```bash
curl "http://127.0.0.1:8000/feeds/FD-1" \
  -H "X-API-Key: demo-secret-key"
```

---

### Example Response

```json
{
  "feed_id": "FD-1",
  "partner_name": "Acme Corp",
  "file_name": "products.csv",
  "status": "uploaded"
}
```

---

### Errors

| Status | Description     |
|--------|-----------------|
| 401    | Missing API key |
| 403    | Invalid API key |
| 404    | Feed not found  |

### Example Not Found Response

```json
{
  "error_code": "FEED_NOT_FOUND",
  "message": "Feed FD-999 not found",
  "details": {
    "feed_id": "FD-999"
  }
}
```
---

## POST /feeds/{feed_id}/validate

Creates a validation job for the specified feed and updates the feed status to `validating`.

### Path Parameters

* `feed_id` *(string, required)* — Unique identifier for the feed

---

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/feeds/FD-1/validate" \
  -H "X-API-Key: demo-secret-key"
```

---

### Example Response

```json
{
  "message": "Validation started",
  "feed_id": "FD-1",
  "job_id": "VJ-1",
  "status": "validating"
}
```

---

### Errors

| Status | Description     |
|--------|-----------------|
| 401    | Missing API key |
| 403    | Invalid API key |
| 404    | Feed not found  |

### Example Not Found Response

```json
{
  "error_code": "FEED_NOT_FOUND",
  "message": "Feed FD-999 not found",
  "details": {
    "feed_id": "FD-999"
  }
}
```
---

## Feed Status Values

| Status     | Description             |
|------------|-------------------------|
| uploaded   | Feed has been submitted |
| validating | Validation in progress  |
| validated  | Feed passed validation  |
| failed     | Feed failed validation  |
