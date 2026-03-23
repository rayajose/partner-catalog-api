# Jobs

## GET /jobs/{job_id}
Retrieve job status

### Path Parameters

* `job_id` *(string, required)* — Unique identifier for the job

### Example Request

```
POST /jobs/j_1
```

### Response (200)

```json
{
  "job_id": "j_1",
  "feed_id": "f_1",
  "status": "queued",
  "job_type": "feed_submission"
}
```