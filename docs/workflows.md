# Workflows

This section demonstrates how to use the API to submit a partner feed, start validation, and track processing status.

---

## Submit and Validate a Feed

This workflow shows the typical sequence for processing a partner product feed.

### Step 1 — Submit a feed

```bash
curl -X POST "http://127.0.0.1:8000/feeds" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_name": "Acme Corp",
    "file_name": "products.csv",
    "submitted_by": "user@example.com",
    "notes": "Initial upload"
  }'
```

Example response:

```json
{
  "feed_id": "FD-1",
  "status": "uploaded",
  "job_id": "SJ-1"
}
```

---

### Step 2 — Start validation

```bash
curl -X POST "http://127.0.0.1:8000/feeds/FD-1/validate"
```

Example response:

```json
{
  "message": "Validation started",
  "feed_id": "FD-1",
  "job_id": "VJ-1",
  "status": "validating"
}
```

---

### Step 3 — Check job status

```bash
curl "http://127.0.0.1:8000/jobs/VJ-1"
```

Example response:

```json
{
  "job_id": "VJ-1",
  "feed_id": "FD-1",
  "status": "running",
  "job_type": "validation"
}
```

---

### Workflow Summary

* A feed is submitted and assigned a `feed_id`
* A job is created to process the feed
* Validation is triggered via a separate endpoint
* Job status can be checked using the Jobs API

---

## Inspecting Feeds (Optional)

The following endpoints are useful for retrieving and filtering feed data but are not required for the core workflow.

---

### Retrieve a specific feed

```bash
curl "http://127.0.0.1:8000/feeds/FD-1"
```

Example response:

```json
{
  "feed_id": "FD-1",
  "partner_name": "Acme Corp",
  "file_name": "products.csv",
  "status": "uploaded"
}
```

---

### List feeds with filtering and pagination

```bash
curl "http://127.0.0.1:8000/feeds?status=uploaded&limit=2&offset=0"
```

Example response:

```json
{
  "items": [
    {
      "feed_id": "FD-1",
      "partner_name": "Acme Corp",
      "file_name": "products.csv",
      "status": "uploaded"
    }
  ],
  "total": 1,
  "limit": 2,
  "offset": 0
}
```

---

## Notes

* Feed IDs use the format `FD-<number>`
* Job IDs use the following format
    * Feed submission: `SJ-<number>`
    * Feed validation: `VJ-<number>`
* This API uses in-memory storage; data resets when the application restarts

---

## Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Errors](errors.md)
