# Python SDK Guide

This guide shows how developers can interact with the Partner Catalog API using a lightweight Python client.

The example client demonstrates an SDK-style approach to working with the API. Instead of writing raw HTTP requests for each operation, developers can use reusable Python methods to upload catalog feeds, check processing jobs, and retrieve product data.

This guide is intended for local development, testing, and portfolio demonstration purposes.

---

## Overview

The Python client provides methods for:

* Uploading partner product feeds
* Checking job status
* Retrieving product data
* Filtering, sorting, and paginating results

---

## Example Files

The Python client and runnable example are available in the repository:

- `examples/sdk/client.py`
- `examples/sdk/example_usage.py`

These files demonstrate how to interact with the API using an SDK-style approach.

---

## Authentication

All requests require an API key passed in the `x-api-key` header.

```python
headers = {
    "x-api-key": "demo-secret-key"
}
```

---

## Install Dependencies

```bash
pip install requests
```

---

## Example Client

```python
import requests

class PartnerCatalogClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": api_key
        }

    def upload_feed(self, partner_name: str, file_path: str):
        url = f"{self.base_url}/feeds/upload"

        with open(file_path, "rb") as csv_file:
            files = {"file": csv_file}
            data = {"partner_name": partner_name}

            response = requests.post(
                url,
                headers=self.headers,
                files=files,
                data=data
            )

        response.raise_for_status()
        return response.json()

    def get_job(self, job_id: str):
        url = f"{self.base_url}/jobs/{job_id}"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()
        return response.json()

    def get_products(
        self,
        partner_name: str = None,
        brand: str = None,
        category: str = None,
        availability: str = None,
        sort_by: str = "created_at",
        order: str = "asc",
        limit: int = 10,
        cursor: str = None
    ):
        url = f"{self.base_url}/products"

        params = {
            "partner_name": partner_name,
            "brand": brand,
            "category": category,
            "availability": availability,
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "cursor": cursor
        }

        params = {k: v for k, v in params.items() if v is not None}

        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        response.raise_for_status()
        return response.json()
```

---

## Usage Example

```python
client = PartnerCatalogClient(
    base_url="http://127.0.0.1:8000",
    api_key="demo-secret-key"
)

response = client.upload_feed(
    partner_name="Running Warehouse",
    file_path="running_shoes.csv"
)

print(response)
```

---

## Check Job Status

```python
job = client.get_job("JS00001")
print(job)
```

---

## Retrieve Products

```python
products = client.get_products(limit=5)
print(products)
```

---

## Filter and Sort Products

```python
products = client.get_products(
    category="Running Shoes",
    availability="in_stock",
    sort_by="price",
    order="asc",
    limit=5
)

print(products)
```

---

## Cursor-Based Pagination

```python
first_page = client.get_products(limit=5)

next_cursor = first_page.get("next_cursor")

if next_cursor:
    second_page = client.get_products(
        limit=5,
        cursor=next_cursor
    )

    print(second_page)
```

---

## Error Handling

The client uses `response.raise_for_status()` to raise exceptions for HTTP errors.

```python
import requests

try:
    products = client.get_products(limit=5)
except requests.exceptions.HTTPError as error:
    print(f"Request failed: {error}")
```

---
## Run the Example Locally

Start the API:

```bash
uvicorn main:app --reload
```
Navigate to the SDK example directory:

```bash
cd examples/sdk
```
Run the example:

```bash
python example_usage.py
```
The script will retrieve product data from the API and print the response.

---

## Notes

This example demonstrates a simple SDK-style client for interacting with the Partner Catalog API.

It is intentionally lightweight and is not distributed as a standalone Python package. Developers can extend this client with additional features such as retries, logging, or custom exception handling.
