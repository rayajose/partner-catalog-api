from fastapi import FastAPI
from routers import feeds, jobs

tags_metadata = [
    {
        "name": "Feeds",
        "description": "Operations for submitting, retrieving, filtering, and validating partner product feeds."
    },
    {
        "name": "Jobs",
        "description": "Operations for checking the status of background processing jobs."
    },
]

app = FastAPI(
    title="Partner Catalog API",
    description="A demo API for partner feed submission, validation, and job tracking.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

app.include_router(feeds.router)
app.include_router(jobs.router)