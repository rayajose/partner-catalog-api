# Screenshots

This section provides visual evidence of the Partner Catalog API running in a production-style AWS environment. The application is containerized with Docker, deployed on Amazon ECS Fargate, and backed by a PostgreSQL database hosted on Amazon RDS. Public access is provided through an Application Load Balancer.

## Live API Documentation
The API is exposed through a public load balancer and provides interactive documentation via Swagger UI.
![swagger-overview.png](screenshots/swagger-overview.png)

## ECS Task Definition and Container Configuration
The task definition specifies the container image from Amazon ECR and runtime configuration, including environment variables used for database connectivity.

### Deployment
![Deployment](screenshots/pcapi-ecs-service-deployment-overview.png)

### Performance Monitoring
![Performance Monitoring](screenshots/pcapi-ecs-service-performance-monitoring.png)

### Tasks
![Tasks](screenshots/pcapi-ecs-service-tasks.png)

## ECS Task Definition
![Task Definition](screenshots/pcapi-ecs-service-task-definition.png)

## Container Details
![Container Details](screenshots/pcapi-ecs-service-container-details.png)

## Amazon ECR Repository
The container image for the API is stored in Amazon Elastic Container Registry and used by ECS during deployment.
![ECR Repo](screenshots/pcapi-ecr-repo.png)

## Application Load Balancer

### Rules and Listeners
![ALB Listeners](screenshots/pcapi-ec2-alb-listeners.png)

### Network Mapping
![ALB Network Map](screenshots/pcapi-ec2-alb-network-mapping.png)

## Target Group Health Checks
The target group monitors the health of running tasks using an HTTP health check endpoint to ensure traffic is only routed to healthy containers.
![Target Group](screenshots/pcapi-ec2-target-group.png)

## Amazon RDS PostgreSQL Database
The API persists data in a PostgreSQL database hosted on Amazon RDS, providing managed storage and availability.
![RDS](screenshots/pcapi-rds.png)

## MkDocs Documentation Site
Project documentation is generated using MkDocs and hosted via GitHub Pages.
