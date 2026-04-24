# Screenshots

This section provides visual evidence of the Partner Catalog API running in a production-style AWS environment. The application is containerized with Docker, deployed on Amazon ECS Fargate, and backed by a PostgreSQL database hosted on Amazon RDS. Public access is provided through an Application Load Balancer.

## Live API Documentation
<p align="center">
  <img src="screenshots/swagger-overview.png" alt="Swagger Overview" width="85%">
</p>

## Health Check Endpoint

The `/health` endpoint verifies API availability and database connectivity. The Application Load Balancer uses this endpoint for target group health checks.

### Path
<p align="center">
  <img src="screenshots/swagger-health-check-path.png" alt="Health Check Path" width="85%">
</p>

### Endpoint
<p align="center">
  <img src="screenshots/swagger-health-check-endpoint.png" alt="Health Check Endpoint" width="85%">
</p>

## ECS Task Definition and Container Configuration
The task definition specifies the container image from Amazon ECR and runtime configuration, including environment variables used for database connectivity.

### Deployment
<p align="center">
  <img src="screenshots/pcapi-ecs-service-deployment-overview.png" alt="Deployment" width="85%">
</p>

### Performance Monitoring
<p align="center">
  <img src="screenshots/pcapi-ecs-service-performance-monitoring.png" alt="Performance Monitoring" width="85%">
</p>

### Tasks
<p align="center">
  <img src="screenshots/pcapi-ecs-service-tasks.png" alt="Tasks" width="85%">
</p>

## ECS Task Definition
<p align="center">
  <img src="screenshots/pcapi-ecs-service-task-definition.png" alt="Task Definition" width="85%">
</p>

## Container Details
<p align="center">
  <img src="screenshots/pcapi-ecs-service-container-details.png" alt="Container Details" width="85%">
</p>

## Amazon ECR Repository
The container image for the API is stored in Amazon Elastic Container Registry and used by ECS during deployment.
<p align="center">
  <img src="screenshots/pcapi-ecr-repo.png" alt="ECR Repo" width="85%">
</p>

## Application Load Balancer

### Rules and Listeners
<p align="center">
  <img src="screenshots/pcapi-ec2-alb-listeners.png" alt="ALB Listeners" width="85%">
</p>

### Network Mapping
<p align="center">
  <img src="screenshots/pcapi-ec2-alb-network-mapping.png" alt="ALB Network Map" width="85%">
</p>

## Target Group Health Checks
The target group monitors the health of running tasks using an HTTP health check endpoint to ensure traffic is only routed to healthy containers.
<p align="center">
  <img src="screenshots/pcapi-ec2-target-group-health-check.png" alt="Target Group Health Checks" width="85%">
</p>

## Amazon RDS PostgreSQL Database
The API persists data in a PostgreSQL database hosted on Amazon RDS, providing managed storage and availability.
<p align="center">
  <img src="screenshots/pcapi-rds.png" alt="RDS" width="85%">
</p>

## MkDocs Documentation Site
Project documentation is generated using MkDocs and hosted via GitHub Pages.
