# Partner Catalog API

A REST API for ingesting, validating, and tracking partner product feeds.

This project demonstrates API design, data modeling, and developer-focused documentation using a realistic e-commerce ingestion workflow.

---

## 🚀 Overview

The Partner Catalog API simulates how large-scale platforms ingest and process partner product data.

It allows clients to:

* Upload product feeds (CSV)
* Validate feed structure
* Track processing via jobs
* Retrieve feed metadata
* Persist data using a database

---

## ✨ Key Features

* 📥 **CSV Feed Upload** via multipart requests
* 🔄 **Job Tracking Model** (submission + validation)
* 💾 **Persistent Storage** (SQLite-backed)
* 🧠 **Structured ID System** (`FDxxx`, `JSxxx`, `JVxxx`)
* 📄 **Comprehensive API Documentation (MkDocs)**
* 🔐 **API Key Authentication**
* 🧩 **Layered Architecture (Router → Store → DB)**

---

## 🏗️ Architecture

```text
Client → FastAPI Router → Data Layer → SQLite Database
```

* **Routers** handle HTTP requests and validation
* **Data layer (`stores.py`)** manages persistence and ID generation
* **SQLite** stores feeds, jobs, and counters

See [Architecture](docs/architecture.md) for full details.

---

## 🔄 Example Workflow

```text
Upload Feed → Create Feed (FD001)
            → Create Submission Job (JS001)
            → Create Validation Job (JV001)

Jobs → Track processing
Feed → Retrieve metadata
```

---

## 📦 API Endpoints

| Method | Endpoint           | Description            |
| ------ | ------------------ | ---------------------- |
| POST   | `/feeds/upload`    | Upload a CSV feed      |
| GET    | `/feeds/{feed_id}` | Retrieve feed metadata |
| GET    | `/jobs/{job_id}`   | Retrieve job status    |

Interactive docs available at:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

All requests require an API key:

```http
X-API-Key: demo-secret-key
```

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Run the API

```bash
uvicorn app.main:app --reload
```

---

### 3. Upload a sample feed

```bash
curl -X POST "http://127.0.0.1:8000/feeds/upload" \
  -H "x-api-key: demo-secret-key" \
  -F "partner_name=Acme Corp" \
  -F "file=@app/test_data/sample_catalog.csv"
```

---

## 📄 Example Response

```json
{
  "feed_id": "FD001",
  "status": "uploaded",
  "job_id": "JS001"
}
```

---

## 📚 Documentation

Full documentation is available in the `docs/` directory:

* [API Overview](docs/index.md)
* [Feeds API](docs/feeds.md)
* [Jobs API](docs/jobs.md)
* [Workflows](docs/workflows.md)
* [Architecture](docs/architecture.md)
* [Errors](docs/errors.md)

---

## 🧠 Design Highlights

* **Separation of concerns** between API, data, and persistence layers
* **Database-backed ID generation** for stable, traceable identifiers
* **API/DB field mapping** (`filename` → `file_name`)
* **Job-based workflow model** to simulate asynchronous processing

---

## 🔮 Future Enhancements

* Store and query product-level data from CSV feeds
* Add filtering and pagination
* Introduce background job processing
* Migrate to PostgreSQL or cloud database
* Add authentication/authorization enhancements

---

## 🛠️ Tech Stack

* FastAPI
* Python
* SQLite
* OpenAPI (Swagger)
* MkDocs

---

## 📊 API Preview

*(Screenshot of Swagger UI will be added after final feature implementation)*

## 📎 Notes

This project is designed as a portfolio piece to demonstrate:

* API design and implementation
* technical documentation skills
* real-world data ingestion patterns

---

## 👤 Author

Ray Jose
Technical Writer | Content Engineer | API Documentation Specialist
