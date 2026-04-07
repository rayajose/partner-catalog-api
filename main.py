from fastapi import FastAPI
from routers import feeds, jobs, products
from db import init_db

tags_metadata = [
    {
        "name": "Feeds",
        "description": "Operations for uploading and retrieving partner product feeds."
    },
    {
        "name": "Jobs",
        "description": "Operations for checking submission and validation job status.."
    },
    {
        "name": "Products",
        "description": "Operations for viewing and filtering products parsed from uploaded CSV feeds."
    }
]

app = FastAPI(
    title="Partner Catalog API",
    description=(
        "A REST API for ingesting, validating, and tracking partner product feeds. "
        "This project demonstrates API design, data modeling, persistence, "
        "and developer-focused documentation."
    ),
    version="0.2.0",
    openapi_tags=tags_metadata,
)

init_db()

app.include_router(feeds.router)
app.include_router(jobs.router)
app.include_router(products.router)