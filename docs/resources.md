# Resources

## Feed

A Feed represents a product data file submitted by a partner.

### Fields

- `feed_id` — unique identifier for the feed
- `partner_name` — name of the submitting partner
- `file_name` — name of the uploaded file
- `status` — current state of the feed

### Status values

- `uploaded`
- `validating`
- `validated`
- `failed`

---

## Job

A Job represents a background process such as feed submission or validation.

### Fields

- `job_id` — unique identifier for the job
- `feed_id` — associated feed
- `status` — current job status
- `job_type` — type of job

### Status values

- `queued`
- `running`
- `completed`
- `failed`