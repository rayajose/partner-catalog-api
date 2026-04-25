"""
Partner Catalog API - Python Client Example

This is a lightweight SDK-style client demonstrating how to interact
with the Partner Catalog API.

Location:
    examples/sdk/client.py
"""

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
        feed_id: str = None,
        sku: str = None,
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
            "feed_id": feed_id,
            "sku": sku,
            "brand": brand,
            "category": category,
            "availability": availability,
            "sort_by": sort_by,
            "order": order,
            "limit": limit,
            "cursor": cursor
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = requests.get(
            url,
            headers=self.headers,
            params=params
        )

        response.raise_for_status()
        return response.json()