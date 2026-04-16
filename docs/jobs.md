# Jobs API

The Jobs API provides visibility into processing operations such as feed submission and validation.

---

## Authentication

All requests must include:

```text id="j1k2l3"
x-api-key: <your-api-key>
```

---

## Get Job

**GET** `/jobs/{job_id}`

Returns status and metadata for a job.

---

### Example Request

```http id="m4n5o6"
GET /jobs/JS00001
```

---

### Response (200 OK)

```json id="p7q8r9"
{
  "job_id": "JS00001",
  "job_type": "submission",
  "status": "completed",
  "created_at": "2026-04-06T14:17:27+00:00",
  "feed_id": "FD00001",
  "message": "Feed upload accepted."
}
```

---

### Field Definitions

| Field      | Type   | Description                                             |
| ---------- | ------ | ------------------------------------------------------- |
| job_id     | string | Unique job identifier (JSxxxxx or JVxxxxx)              |
| job_type   | string | Type of job (`submission`, `validation`)                |
| status     | string | Job status (`queued`, `running`, `completed`, `failed`) |
| created_at | string | UTC timestamp when job was created                      |
| feed_id    | string | Associated feed ID                                      |
| message    | string | Optional status message                                 |

---

### Job Types

| Type       | Description                          |
| ---------- | ------------------------------------ |
| submission | Feed upload processing               |
| validation | CSV structure and content validation |

---

### Job Lifecycle

Jobs simulate asynchronous processing and may transition through the following states:

* `queued` → job created and awaiting processing
* `running` → job actively processing
* `completed` → job finished successfully
* `failed` → job encountered an error

---

### Error Responses

#### 404 Not Found

```json id="s1t2u3"
{
  "detail": "Job JS99999 not found."
}
```

---

## Related Endpoints

* `POST /feeds/upload` — creates submission and validation jobs
* `GET /feeds/{feed_id}` — retrieve feed associated with jobs
