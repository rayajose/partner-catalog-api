# Jobs

## GET /jobs/{job_id}
Returns the current status and details of a processing job.

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

### Status values
A job moves through the following states:
- queued
- running
- completed
- failed

### Behavior

- `queued` → created but not yet started  
- `running` → actively processing  
- `completed` → successfully finished  
- `failed` → terminated with error  