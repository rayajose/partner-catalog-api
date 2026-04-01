# Jobs API

Jobs represent background processing tasks such as feed submission and validation.

---

## GET /jobs/{job_id}

Returns the current status and details of a processing job.

### Path Parameters

* `job_id` *(string, required)* — Unique identifier for the job

---

### Example Request

```bash
curl "http://127.0.0.1:8000/jobs/VJ-1" \
  -H "X-API-Key: demo-secret-key"
```

---

### Example Response

```json
{
  "job_id": "VJ-1",
  "feed_id": "FD-1",
  "status": "running",
  "job_type": "validation"
}
```

---

### Response Fields

* `job_id` *(string)* — Unique job identifier
* `feed_id` *(string)* — Associated feed
* `status` *(string)* — Current job status
* `job_type` *(string)* — Type of job

---

### Errors

| Status | Description     |
|--------|-----------------|
| 401    | Missing API key |
| 403    | Invalid API key |
| 404    | Job not found   |

### Example Not Found Response

```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job VJ-999 not found",
  "details": {
    "job_id": "VJ-999"
  }
}
```
---

## Job Status Values

| Status    | Description                    |
|-----------|--------------------------------|
| queued    | Job is waiting to be processed |
| running   | Job is currently executing     |
| completed | Job completed successfully     |
| failed    | Job failed                     |
