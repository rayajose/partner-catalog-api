# Feeds API

The Feeds API allows clients to upload and retrieve product feed metadata. Feed uploads are validated and tracked using asynchronous job records.

---

## 🔐 Authentication

All requests must include an API key in the header:

```
x-api-key: <your-api-key>
```

---

## 📥 Upload Feed

**POST** `/feeds/upload`

Uploads a CSV product feed and creates associated job records.

### Request

**Headers**

```
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

```
curl -X POST http://127.0.0.1:8000/feeds/upload \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

---

### Response (201 Created)

```json
{
  "feed_id": "FD001",
  "status": "uploaded",
  "job_id": "JS001"
}
```

---

### Behavior

* Validates file type (CSV only)
* Validates CSV structure (header row required)
* Creates:

  * **Submission Job (JSxxx)** → tracks upload
  * **Validation Job (JVxxx)** → tracks CSV validation
* Persists feed metadata to database

---

### Error Responses

#### 400 Bad Request

```json
{
  "detail": "Only CSV uploads are supported at this time."
}
```

```json
{
  "detail": "Uploaded file is empty."
}
```

```json
{
  "detail": "Invalid CSV file: CSV header row is missing."
}
```

---

## 📄 Get Feed

**GET** `/feeds/{feed_id}`

Returns metadata for a specific feed.

---

### Example Request

```
GET /feeds/FD001
```

---

### Response (200 OK)

```json
{
  "feed_id": "FD001",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV001"
}
```

---

### Field Definitions

| Field             | Type   | Description                                 |
| ----------------- | ------ | ------------------------------------------- |
| feed_id           | string | Unique feed identifier (FDxxx)              |
| partner_name      | string | Partner that submitted the feed             |
| file_name         | string | Original uploaded file name                 |
| content_type      | string | MIME type of uploaded file                  |
| status            | string | Feed status (`uploaded`, `validated`, etc.) |
| uploaded_at       | string | UTC timestamp of upload                     |
| validation_job_id | string | Job ID for validation process (JVxxx)       |

---

### Error Responses

#### 404 Not Found

```json
{
  "detail": "Feed FD999 not found."
}
```
