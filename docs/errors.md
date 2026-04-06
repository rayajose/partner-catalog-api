# Errors

This section describes how errors are returned by the Partner Catalog API.

---

## 📌 Error Format

The API uses FastAPI’s standard error response format.

### Format

```json
{
  "detail": "Human-readable error message"
}
```

### Fields

| Field  | Type   | Description                        |
| ------ | ------ | ---------------------------------- |
| detail | string | Description of the error condition |

---

## 🔍 Common Error Scenarios

Errors may occur in the following situations:

* Missing or invalid API key
* Invalid request data (e.g., malformed CSV)
* Resource not found (feed or job does not exist)

---

## 📊 Status Codes

| Status | Meaning                             |
| ------ | ----------------------------------- |
| 200    | Request completed successfully      |
| 201    | Resource created successfully       |
| 400    | Bad request (invalid input or file) |
| 401    | Missing API key                     |
| 403    | Invalid API key                     |
| 404    | Requested resource not found        |
| 422    | Request validation failed           |
| 500    | Internal server error               |

---

## 🔐 Authentication Errors

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

## 📄 Resource Errors

### 404 Not Found

Returned when a requested resource does not exist.

#### Example: Feed not found

```json
{
  "detail": "Feed FD999 not found."
}
```

#### Example: Job not found

```json
{
  "detail": "Job JS999 not found."
}
```

---

## ⚠️ Validation Errors

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

## 🧠 Design Notes

* The API uses FastAPI’s built-in error handling for consistency and simplicity
* All error responses use the `detail` field
* Resource identifiers follow structured formats:

  * `FDxxx` → Feed
  * `JSxxx` → Submission Job
  * `JVxxx` → Validation Job
* Custom error formats may be introduced in future versions if needed for client-side handling

---

## 🔗 Related Documentation

* [Feeds API](feeds.md)
* [Jobs API](jobs.md)
