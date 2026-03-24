# Workflows

## Submit and Validate a Feed

### Step 1: Create a feed

POST /feeds

### Step 2: Start validation

POST /feeds/{feed_id}/validate

### Step 3: Check job status

GET /jobs/{job_id}