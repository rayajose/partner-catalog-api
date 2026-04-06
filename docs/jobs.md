# Jobs API

The Jobs API provides visibility into processing operations such as feed submission and validation.

---

## 🔐 Authentication

All requests must include:

```
x-api-key: <your-api-key>
```

---

## 📄 Get Job

**GET** `/jobs/{job_id}`

Returns status and metadata for a job.

---

### Example Request

```
GET /jobs/JS001
```

---

### Response (200 OK)

```json
{
  "job_id": "JS001",
  "job_type": "submission",
  "status": "completed",
  "created_at": "2026-04-06T14:17:27+00:00",
  "feed_id": "FD001",
  "message": "Feed upload accepted."
}
```

---

### Field Definitions

| Field      | Type   | Description                                   |
| ---------- | ------ | --------------------------------------------- |
| job_id     | string | Unique job identifier (JSxxx or JVxxx)        |
| job_type   | string | Type of job (`submission`, `validation`)      |
| status     | string | Job status (`pending`, `completed`, `failed`) |
| created_at | string | UTC timestamp when job was created            |
| feed_id    | string | Associated feed ID                            |
| message    | string | Optional status message                       |

---

### Job Types

| Type       | Description              |
| ---------- | ------------------------ |
| submission | Feed upload processing   |
| validation | CSV structure validation |

---

### Error Responses

#### 404 Not Found

```json
{
  "detail": "Job JS999 not found."
}
```
