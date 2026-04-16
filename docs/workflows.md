# Workflows

This section demonstrates how to use the API to upload a partner feed, track processing jobs, and retrieve product data.

---

## Submit and Process a Feed

This workflow shows the typical sequence for ingesting a partner product feed and making the data available for querying.

---

### Step 1 — Upload a feed

```bash id="wf1"
curl -X POST "http://127.0.0.1:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@sample_catalog.csv"
```

---

### Example Response

```json id="wf2"
{
  "feed_id": "FD00001",
  "status": "uploaded",
  "job_id": "JS00001"
}
```

---

### What happens

* The feed is stored in the system
* A **submission job (JSxxxxx)** is created
* A **validation job (JVxxxxx)** is created
* CSV data is parsed and product records are stored
* Feed metadata is persisted in the database

---

### Step 2 — Check submission job

```bash id="wf3"
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/jobs/JS00001"
```

---

### Example Response

```json id="wf4"
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

### Step 3 — Check validation job

```bash id="wf5"
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/jobs/JV00001"
```

---

### Example Response

```json id="wf6"
{
  "job_id": "JV00001",
  "job_type": "validation",
  "status": "completed",
  "created_at": "2026-04-06T14:17:27+00:00",
  "feed_id": "FD00001",
  "message": "CSV validation completed."
}
```

---

### Step 4 — Retrieve feed metadata

```bash id="wf7"
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/feeds/FD00001"
```

---

### Example Response

```json id="wf8"
{
  "feed_id": "FD00001",
  "partner_name": "Acme Corp",
  "file_name": "sample_catalog.csv",
  "content_type": "text/csv",
  "status": "uploaded",
  "uploaded_at": "2026-04-06T14:17:27+00:00",
  "validation_job_id": "JV00001"
}
```

---

### Step 5 — Query products

```bash id="wf9"
curl -H "x-api-key: demo-secret-key" \
  "http://127.0.0.1:8000/products?limit=5"
```

---

### Example Response

```json id="wf10"
{
  "count": 5,
  "items": [
    {
      "product_id": "PR00001",
      "feed_id": "FD00001",
      "partner_name": "Acme Corp",
      "sku": "AC-1001",
      "product_name": "Sample Product",
      "price": 49.99,
      "currency": "USD",
      "availability": "in_stock",
      "created_at": "2026-04-08T12:00:00Z"
    }
  ],
  "next_cursor": "PR00005"
}
```

---

## Workflow Summary

```text id="wf11"
Upload Feed → Create Feed (FDxxxxx)
            → Create Submission Job (JSxxxxx)
            → Create Validation Job (JVxxxxx)
            → Parse and store products (PRxxxxx)

Jobs → Track processing status
Feed → Retrieve metadata
Products → Query catalog data
```

---

## Key Points

* Feed upload is handled via a single endpoint: `/feeds/upload`
* Validation is automatically triggered (no separate endpoint required)
* Jobs provide traceability for processing steps
* Product data is parsed and stored during ingestion
* All data is persisted in a relational database
* IDs follow structured formats:

  * `FDxxxxx` → Feed
  * `JSxxxxx` → Submission Job
  * `JVxxxxx` → Validation Job
  * `PRxxxxx` → Product

---

## Notes

* Validation checks CSV structure and basic data integrity
* Jobs are executed synchronously but modeled as asynchronous processes
* Product data becomes immediately queryable after ingestion

---

## Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Products API](products.md)
* [Errors](errors.md)
