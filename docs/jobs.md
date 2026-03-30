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
curl "http://127.0.0.1:8000/jobs/j_2"
```

---

### Example Response

```json
{
  "job_id": "j_2",
  "feed_id": "f_1",
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

| Status | Description   |
|--------|---------------|
| 404    | Job not found |

### Example Not Found Response

```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job j_999 not found",
  "details": {
    "job_id": "j_999"
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
