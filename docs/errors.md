# Errors

## Standard error model
All non-success responses use the following structure:
```json
{
  "error_code": "STRING_CODE",
  "message": "Human-readable summary",
  "details": {
    "field": "value"
  }
}
```
### Example: feed not found
```json
{
  "error_code": "FEED_NOT_FOUND",
  "message": "Feed 12345 not found",
  "details": {
    "feed_id": "12345"
  }
}
```
### Example: job not found
```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job 98765 not found",
  "details": {
    "job_id": "98765"
  }
}
```