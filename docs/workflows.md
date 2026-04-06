# Workflows

This section demonstrates how to use the API to upload a partner feed, track processing jobs, and retrieve feed metadata.

---

## 🔄 Submit and Process a Feed

This workflow shows the typical sequence for ingesting a partner product feed.

---

### Step 1 — Upload a feed

```bash
curl -X POST "http://127.0.0.1:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

---

### Example Response

```json
{
  "feed_id": "FD001",
  "status": "uploaded",
  "job_id": "JS001"
}
```

---

### What happens

* The feed is stored in the system
* A **submission job (JSxxx)** is created
* A **validation job (JVxxx)** is created
* Feed metadata is persisted in the database

---

### Step 2 — Check submission job

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/jobs/JS001"
```

---

### Example Response

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

### Step 3 — Check validation job

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/jobs/JV001"
```

---

### Example Response

```json
{
  "job_id": "JV001",
  "job_type": "validation",
  "status": "completed",
  "created_at": "2026-04-06T14:17:27+00:00",
  "feed_id": "FD001",
  "message": "CSV structure validation completed."
}
```

---

### Step 4 — Retrieve feed metadata

```bash
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/feeds/FD001"
```

---

### Example Response

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

## 📊 Workflow Summary

```text
Upload Feed → Create Feed (FDxxx)
            → Create Submission Job (JSxxx)
            → Create Validation Job (JVxxx)

Jobs → Track processing status
Feed → Retrieve metadata
```

---

## 🧠 Key Points

* Feed upload is handled via a single endpoint: `/feeds/upload`
* Validation is automatically triggered (no separate endpoint required)
* Jobs provide traceability for processing steps
* All data is persisted in a database
* IDs follow structured formats:

  * `FDxxx` → Feed
  * `JSxxx` → Submission Job
  * `JVxxx` → Validation Job

---

## ⚠️ Notes

* Validation currently checks CSV structure only (header presence and format)
* Jobs are executed synchronously but modeled as asynchronous processes
* Product-level data storage is planned for a future enhancement

---

## 🔗 Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Errors](errors.md)
