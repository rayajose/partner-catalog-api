# Feeds

Represents a partner-submitted product data file. Each feed goes through a lifecycle:

`uploaded → validating → validated → failed`

See [Feed resource](resources.md#feed) for full field definitions.

---

## POST /feeds

Creates a new feed and initiates a submission job.

### Fields

* `partner_name` *(string, required)* — Name of the submitting partner
* `file_name` *(string, required)* — Name of the uploaded file
* `submitted_by` *(string, required)* — User submitting the feed
* `notes` *(string, optional)* — Additional context or comments

### Request Body

```json
{
  "partner_name": "Any Company",
  "file_name": "products.csv",
  "submitted_by": "Michelle Smith",
  "notes": "list of new products"
}
```

### Response (200)

```json
{
  "feed_id": "f_1",
  "status": "uploaded",
  "job_id": "j_1"
}
```

### Errors

| Status | Description          |
| ------ | -------------------- |
| 400    | Invalid request body |
| 422    | Validation error     |

---
See [Errors](errors.md) for error format.

## GET /feeds

Returns a list of feeds, optionally filtered by `status`, with simple pagination.

### Query Parameters

* `status` *(optional)* — Filter by feed status
* `limit` *(integer, optional, default: 10)* — Max number of results
* `offset` *(integer, optional, default: 0)* — Number of results to skip

### Request

```
GET /feeds?status=uploaded&limit=10&offset=0
```
The response includes pagination metadata to support client-side paging and navigation.

### Response Fields

* `items` *(array of Feed)* — List of feed objects
* `total` *(integer)* — Total number of matching feeds (before pagination)
* `limit` *(integer)* — Maximum number of items returned
* `offset` *(integer)* — Number of items skipped

---

### Pagination Behavior

* Results are returned in the order they were created
* Use `offset` to skip items
* Use `limit` to control page size


### Response (200)

```json
{ 
 "items": [
  {
    "feed_id": "f_1",
    "partner_name": "Any Company",
    "file_name": "anyCompany_products.csv",
    "status": "uploaded"
  },
  {
      "feed_id": "Any Other Company",
      "partner_name": "string",
      "file_name": "anyOtherCompany_products.csv",
      "status": "uploaded"
    }
  ],
  "total": 3,
  "limit": 10,
  "offset": 0
}
```

### Errors

| Status | Description              |
| ------ | ------------------------ |
| 400    | Invalid query parameters |

See [Errors](errors.md) for error format.
---

## GET /feeds/{feed_id}

Returns a specific feed.

### Path Parameters

* `feed_id` *(string, required)* — Unique identifier for the feed

### Example Request

```
GET /feeds/f_1
```

### Response (200)

```json
[
  {
    "feed_id": "f_1",
    "partner_name": "Any Company",
    "file_name": "products.csv",
    "status": "uploaded"
  }
]
```

### Errors

| Status | Description    |
| ------ | -------------- |
| 404    | Feed not found |

See [Errors](errors.md) for error format.

#### Example Error

```json
{
  "error_code": "FEED_NOT_FOUND",
  "message": "Feed f_1 not found",
  "details": {
    "feed_id": "f_1"
  }
}
```

---

## POST /feeds/{feed_id}/validate

Starts validation for a feed.

### Path Parameters

* `feed_id` *(string, required)* — Unique identifier for the feed

### Example Request

```
POST /feeds/f_1/validate
```

### Response (200)

```json
{
  "message": "Validation started",
  "feed_id": "f_1",
  "job_id": "j_1",
  "status": "validating"
}
```

### Behavior

* Creates a validation job
* Updates feed status to `validating`
* Validation runs asynchronously

### Errors

| Status | Description                             |
| ------ | --------------------------------------- |
| 404    | Feed not found                          |
| 409    | Feed is already validating or processed |

---
See [Errors](errors.md) for error format.

## Feed Lifecycle

Feeds move through the following states:

| Status     | Description               |
| ---------- | ------------------------- |
| uploaded   | Feed has been submitted   |
| validating | Validation is in progress |
| validated  | Feed passed validation    |
| failed     | Feed failed validation    |

---

## Workflow Example

### Submit and validate a feed

1. Create a feed
   `POST /feeds`

2. Start validation
   `POST /feeds/{feed_id}/validate`

3. Check job status
   `GET /jobs/{job_id}`
