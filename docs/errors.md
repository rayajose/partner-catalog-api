# Errors

This API currently uses two error formats:

1. **Custom application errors** for domain-specific cases such as missing feeds or jobs
2. **Default FastAPI validation errors** for invalid request data

---

## Custom Application Error Format

Some endpoints return a custom JSON error payload for application-specific failures such as resource-not-found conditions.

### Format

```json
{
  "error_code": "STRING_CODE",
  "message": "Human-readable summary",
  "details": {
    "field": "value"
  }
}
```

### Fields

* `error_code` *(string)* — Machine-readable error identifier
* `message` *(string)* — Human-readable summary
* `details` *(object, optional)* — Additional context for debugging or client handling


---

## FastAPI Validation Error Format

When request data fails validation, FastAPI returns its default validation error structure.

This commonly occurs when:

* a required field is missing
* a field has the wrong type
* `submitted_by` is not a valid email address

### Format

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Validation message",
      "type": "validation_error_type"
    }
  ]
}
```

### Fields

* `detail` *(array)* — List of validation problems
* `loc` *(array)* — Location of the invalid value, such as request body or query parameter
* `msg` *(string)* — Human-readable validation message
* `type` *(string)* — Validation error type

---

## Common Status Codes

| Status | Meaning                             |
|--------|-------------------------------------|
| 200    | Request completed successfully      |
| 401    | Missing API key                     |
| 403    | Invalid API key                     |
| 404    | Requested feed or job was not found |
| 422    | Request validation failed           |

---


### 401 Unauthorized

Returned when the API key is missing from the request.

#### Example Response

```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden



Returned when the API key is provided but invalid.

#### Example Response

```json
{
  "detail": "Invalid or missing API key"
}
```

### 404 Not Found

Returned when a requested resource does not exist.

#### Example: Feed not found

```json
{
  "error_code": "FEED_NOT_FOUND",
  "message": "Feed FD-1 not found",
  "details": {
    "feed_id": "FD-1"
  }
}
```

#### Example: Job not found

```json
{
  "error_code": "JOB_NOT_FOUND",
  "message": "Job SJ-1 not found",
  "details": {
    "job_id": "SJ-1"
  }
}
```
### 422 Validation Error

Returned when request data fails validation.

#### Example: Invalid email

```json
{
  "detail": [
    {
      "loc": ["body", "submitted_by"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```
#### Example: Invalid query parameter

```json
{
  "detail": [
    {
      "loc": ["query", "offset"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
}
```
## Notes

* Resource-not-found responses currently use the custom application error format.
* Request validation failures currently use FastAPI’s default validation error format.
* These formats are intentionally documented separately because they are generated differently.

---

## Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Workflows](workflows.md)
