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


#####