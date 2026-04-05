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
curl "http://127.0.0.1:8000/jobs/JV001" \
  -H "X-API-Key: demo-secret-key"
```

---

### Example Response

```json
{
  "job_id": "JV001",
  "feed_id": "FD001",
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
  "message": "Job JV001 not found",
  "details": {
    "job_id": "JV001"
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

## Job ID Format

Job IDs are prefixed by job type: (PLACEHOLDER FOR LATER UPDATE)

- `JS<number>` — feed submission job
- `JV<number>` — feed validation job