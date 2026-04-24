# Deployment Guide — Partner Catalog API

This document describes how the Partner Catalog API is deployed to AWS using a containerized architecture.

---

## Architecture Overview

The application is deployed using the following AWS services:

* FastAPI (Docker container)
* Amazon ECS (Fargate) — container orchestration
* Amazon RDS (PostgreSQL) — relational database
* Application Load Balancer (ALB) — public HTTP access
* Amazon ECR — container image registry

---

## Container Configuration

**Image URI**

```text
792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

**Container Port**

```text
8000
```

---

## ECS Service Configuration

* Launch type: Fargate
* Desired tasks: 1 (set to 0 when not in use)
* Deployment type: Rolling update
* Load balanced: Yes

---

## Networking

* VPC: `vpc-03a81166f39b94bd9`
* Subnets:

  * `subnet-0397a6bfd705d1c76`
  * `subnet-07a21f9409bffa8e9`
* Auto-assign public IP: Enabled

**ECS Security Group**

```text
sg-00778f0b6fabbf1af
```

* Allows outbound traffic to RDS and internet
* Used as the trusted source for database access

---

## Load Balancer (ALB)

**DNS Name**

```text
http://partner-catalog-alb-1398338240.us-east-2.elb.amazonaws.com
```

**Listener**

* HTTP :80 → Target Group

**Target Group**

* Protocol: HTTP
* Port: 8000
* Health check path: `/docs`

---

## Database (RDS PostgreSQL)

* Engine: PostgreSQL
* Port: 5432
* Database name: `partner_catalog`

### Security Group

```text
sg-07a78daece2d2cf47
```

**Inbound Rules**

* PostgreSQL (5432) from ECS security group:

  ```
  sg-00778f0b6fabbf1af
  ```
* PostgreSQL (5432) from developer IP (optional)

**Important**

* RDS is not publicly accessible
* Only ECS tasks are allowed to connect

---

## Environment Variables

Configured in ECS task definition:

```text
DB_TYPE=postgres
DB_HOST=<rds-endpoint>
DB_PORT=5432
DB_NAME=partner_catalog
DB_USER=postgres
DB_PASSWORD=<secured>
```

---

## Deployment Workflow

### 1. Authenticate to ECR

```bash
aws ecr get-login-password --region us-east-2 \
| docker login --username AWS --password-stdin 792233688886.dkr.ecr.us-east-2.amazonaws.com
```

### 2. Build Docker Image

```bash
docker build -t partner-catalog-api .
```

### 3. Tag Image

```bash
docker tag partner-catalog-api:latest \
792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

### 4. Push to ECR

```bash
docker push 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

### 5. Deploy to ECS

* Update ECS service
* Enable **Force new deployment**

---

## Start / Stop Workflow (Cost Control)

### Stop the application

1. ECS → Service → Update

2. Set **Desired tasks = 0**

3. Deploy

4. RDS → Actions → **Stop temporarily**

---

### Start the application

1. RDS → **Start database**
2. Wait until status = **Available**
3. ECS → Service → Update
4. Set **Desired tasks = 1**
5. Deploy

---

## Health Check Behavior

* ALB checks `/docs`
* Container must start successfully and connect to DB
* If DB is unreachable, container exits and task fails

---

## Troubleshooting

### Container fails to start

**Symptom**

* `CannotPullContainerError`

**Cause**

* Image not found in ECR

**Fix**

* Build, tag, and push image with correct tag

---

### Container exits immediately

**Symptom**

* Exit code 1

**Cause**

* Application startup failure (often DB connection)

**Fix**

* Verify environment variables
* Verify RDS connectivity

---

### Database connection timeout

**Error**

```
psycopg.errors.ConnectionTimeout
```

**Cause**

* RDS security group does not allow ECS traffic

**Fix**

* Add ECS security group to RDS inbound rules (port 5432)

---

## Cost Notes

This architecture incurs cost from:

* ECS Fargate (compute)
* RDS (database instance)
* ALB (load balancer)

To minimize cost:

* Stop ECS service when not in use
* Stop RDS when not in use (auto-restarts after ~7 days)
* Keep snapshots for backup instead of running DB continuously

---

## Notes

* Application initializes database schema at startup (`init_db()`)
* Database must be reachable for container to start successfully
* Single-task deployment may have brief downtime during updates

---
For deployment evidence, see [Screenshots](screenshots.md).