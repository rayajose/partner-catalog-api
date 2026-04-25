from client import PartnerCatalogClient


client = PartnerCatalogClient(
    base_url="http://127.0.0.1:8000",
    api_key="demo-secret-key"
)

products = client.get_products(
    limit=5,
    sort_by="created_at",
    order="asc"
)

print(products)