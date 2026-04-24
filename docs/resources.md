# Resources

This section defines the core resources used by the Partner Catalog API.

---

## Feed

A Feed represents a product data file submitted by a partner for ingestion.

### Fields

* `feed_id` — unique identifier for the feed (FDxxxxx)
* `partner_name` — name of the submitting partner
* `file_name` — name of the uploaded file
* `content_type` — MIME type of the uploaded file
* `status` — current state of the feed
* `uploaded_at` — timestamp when the feed was uploaded
* `validation_job_id` — associated validation job ID (JVxxxxx)

---

### Status Values

| Status     | Description                   |
|------------|-------------------------------|
| uploaded   | Feed successfully received    |
| validating | Feed is undergoing validation |
| validated  | Feed passed validation        |
| failed     | Feed failed validation        |

---

## Job

A Job represents a processing task such as feed submission or validation.

Jobs provide visibility into the ingestion workflow and simulate asynchronous processing.

### Fields

* `job_id` — unique identifier for the job (JSxxxxx or JVxxxxx)
* `feed_id` — associated feed
* `job_type` — type of job
* `status` — current job status
* `created_at` — timestamp when the job was created
* `message` — optional status or result message

---

### Job Types

| Type       | Description                          |
|------------|--------------------------------------|
| submission | Feed upload processing               |
| validation | CSV structure and content validation |

---

### Status Values

| Status    | Description                         |
|-----------|-------------------------------------|
| queued    | Job created and awaiting processing |
| running   | Job currently in progress           |
| completed | Job completed successfully          |
| failed    | Job encountered an error            |

---

## Product

A Product represents a normalized item derived from a partner feed.

Products are parsed from uploaded CSV files and stored for querying.

### Fields

* `product_id` — unique identifier for the product (PRxxxxx)
* `feed_id` — associated feed
* `partner_name` — originating partner
* `sku` — partner-defined stock keeping unit
* `product_name` — display name of the product
* `description` — product description
* `brand` — product brand
* `category` — product category
* `price` — product price (numeric)
* `currency` — currency code (e.g., USD)
* `availability` — availability status (e.g., in_stock)
* `created_at` — timestamp when product was ingested

---

## Identifier Format

All resources use structured identifiers for consistency and traceability:

| Prefix | Resource       | Example |
|--------|----------------|---------|
| FD     | Feed           | FD00001 |
| JS     | Submission Job | JS00001 |
| JV     | Validation Job | JV00001 |
| PR     | Product        | PR00001 |

---

## Health Endpoint

Used to verify API and database availability.

### GET /health

Returns the operational status of the API.

**Response**

```json
{
  "status": "ok",
  "database": "connected"
}
```
---

## Notes

* All resources use `snake_case` field naming in API responses
* Identifiers are generated using database-backed counters
* Resources are designed to support scalable ingestion and querying workflows
* Products are derived from feeds but can be queried independently
