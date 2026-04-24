from fastapi import FastAPI
from routers import feeds, jobs, products
from db import init_db

tags_metadata = [
    {
        "name": "Feeds",
        "description": "Upload and manage partner product feeds. Feeds are ingested and validated before products are made available for querying."
    },
    {
        "name": "Jobs",
        "description": "Track background processing jobs for feed submission and validation. Jobs provide status and error visibility."
    },
    {
        "name": "Products",
        "description": "Query the product catalog using filtering, sorting, and cursor-based pagination."
    },
]

app = FastAPI(
    title="Partner Catalog API",

    description=(
        "A REST API for ingesting partner product feeds, validating data, "
        "tracking processing jobs, and querying a centralized product catalog.\n\n"
        "This project demonstrates real-world API design, including:\n"
        "- File-based data ingestion (CSV uploads)\n"
        "- Background job tracking\n"
        "- Structured error handling\n"
        "- Filtering, sorting, and pagination\n"
        "- Deployment to AWS (ECS Fargate + RDS)\n\n"
        "Authentication is handled via an API key passed in the `X-API-Key` header."
    ),
    version="0.1.0",
    contact={
        "name": "Ray Jose",
        "url": "https://github.com/rayajose/partner-catalog-api",
        "email": "ray.a.jose@gmail.com",
        },
license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
        },
    openapi_tags=tags_metadata,
)

init_db()

app.include_router(feeds.router, tags=["Feeds"])
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(products.router, tags=["Products"])