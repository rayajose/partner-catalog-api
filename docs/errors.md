# Errors

This section describes how errors are returned by the Partner Catalog API.

---

## Error Format

The API primarily uses FastAPI’s standard error response format.

### Format

```json
{
  "detail": "Human-readable error message"
}
```

### Fields

| Field  | Type   | Description                        |
|--------|--------|------------------------------------|
| detail | string | Description of the error condition |

---

## Common Error Scenarios

Errors may occur in the following situations:

* Missing or invalid API key
* Invalid request data (e.g., malformed CSV)
* Resource not found (feed, job, or product does not exist)
* Database or infrastructure issues

---

## Status Codes

| Status | Meaning                             |
|--------|-------------------------------------|
| 200    | Request completed successfully      |
| 201    | Resource created successfully       |
| 400    | Bad request (invalid input or file) |
| 401    | Missing API key                     |
| 403    | Invalid API key                     |
| 404    | Requested resource not found        |
| 422    | Request validation failed           |
| 500    | Internal server error               |

---

## Authentication Errors

### 401 Unauthorized

Returned when the API key is missing.

#### Example

```json
{
  "detail": "Not authenticated"
}
```

---

### 403 Forbidden

Returned when the API key is invalid.

#### Example

```json
{
  "detail": "Invalid or missing API key"
}
```

---

## Resource Errors

### 404 Not Found

Returned when a requested resource does not exist.

#### Example: Feed not found

```json
{
  "detail": "Feed FD99999 not found."
}
```

#### Example: Job not found

```json
{
  "detail": "Job JS99999 not found."
}
```

#### Example: Product not found

```json
{
  "detail": "Product PR99999 not found."
}
```

---

## Validation Errors

### 400 Bad Request

Returned when the request is syntactically valid but fails business rules.

#### Example: Unsupported file type

```json
{
  "detail": "Only CSV uploads are supported at this time."
}
```

#### Example: Empty file

```json
{
  "detail": "Uploaded file is empty."
}
```

#### Example: Invalid CSV

```json
{
  "detail": "Invalid CSV file: CSV header row is missing."
}
```

---

### 422 Unprocessable Entity

Returned when request data fails validation (handled by FastAPI).

#### Example

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Validation error message",
      "type": "validation_error_type"
    }
  ]
}
```

---

## Infrastructure Errors

### 500 Internal Server Error

Returned when an unexpected server-side error occurs.

#### Example scenarios

* Database connection failure
* Unhandled application exception
* Misconfigured environment variables

#### Example

```json
{
  "detail": "Internal server error"
}
```

---

## Design Notes

* The API uses FastAPI’s built-in error handling for consistency and simplicity

* Most error responses use the `detail` field

* Validation errors (`422`) use a structured list format defined by FastAPI

* Resource identifiers follow structured formats:

  * `FDxxxxx` → Feed
  * `JSxxxxx` → Submission Job
  * `JVxxxxx` → Validation Job
  * `PRxxxxx` → Product

* Errors are designed to be predictable and human-readable for easier debugging

---

## Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
* [Products API](products.md)
