# Feeds API

The Feeds API allows clients to upload and retrieve product feed metadata. Feed uploads are validated, processed, and stored, with processing tracked using job records.

---

## Authentication

All requests must include an API key in the header:

```id="f1a2b3"
x-api-key: <your-api-key>
```

---

## Upload Feed

**POST** `/feeds/upload`

Uploads a CSV product feed, validates its structure, and creates associated job records.

---

### Request

**Headers**

```id="h4c5d6"
x-api-key: demo-secret-key
Content-Type: multipart/form-data
```

**Form Data**

| Field        | Type   | Required | Description                  |
| ------------ | ------ | -------- | ---------------------------- |
| partner_name | string | yes      | Name of the partner          |
| file         | file   | yes      | CSV file containing products |

---

### Example Request (curl)

```bash id="e7f8g9"
curl -X POST http://127.0.0.1:8000/feeds/upload \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

---

### Response (201 Created)

```json id="i1j2k3"
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "job_id": "JS00001"
}
```

---

### Behavior

* Validates file type (CSV only)

* Validates CSV structure (header row required)

* Creates:

  * **Submission Job (JSxxxxx)** → tracks upload processing
  * **Validation Job (JVxxxxx)** → tracks CSV validation

* Parses and stores product data in the database

* Persists feed metadata for later retrieval

---

### Error Responses

#### 400 Bad Request

```json id="l4m5n6"
{
  "detail": "Only CSV uploads are supported at this time."
}
```

```json id="o7p8q9"
{
  "detail": "Uploaded file is empty."
}
```

```json id="r1s2t3"
{
  "detail": "Invalid CSV file: CSV header row is missing."
}
```

---

## Get Feed

**GET** `/feeds/{feed_id}`

Returns metadata for a specific feed.

---

### Example Request

```http id="u4v5w6"
GET /feeds/FD00001
```

---

### Response (200 OK)

```json id="x7y8z9"
{
  "feed_id": "FD00001",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV00001"
}
```

---

### Field Definitions

| Field             | Type   | Description                                 |
| ----------------- | ------ | ------------------------------------------- |
| feed_id           | string | Unique feed identifier (FDxxxxx)            |
| partner_name      | string | Partner that submitted the feed             |
| file_name         | string | Original uploaded file name                 |
| content_type      | string | MIME type of uploaded file                  |
| status            | string | Feed status (`uploaded`, `validated`, etc.) |
| uploaded_at       | string | UTC timestamp of upload                     |
| validation_job_id | string | Job ID for validation process (JVxxxxx)     |

---

### Error Responses

#### 404 Not Found

```json id="a2b3c4"
{
  "detail": "Feed FD99999 not found."
}
```

---

## Related Endpoints

* `GET /feeds` — List all feeds
* `GET /jobs/{job_id}` — Retrieve job status for associated jobs
* `GET /products/by-feed/{feed_id}` — Retrieve products associated with a feed
