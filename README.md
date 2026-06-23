# DevOps Task Manager Application

## Project Overview

This project demonstrates the deployment of a Flask-based Task Manager application using DevOps best practices. The application is containerized using Docker, deployed on AWS EC2, connected to AWS RDS MySQL, and automated through a Jenkins CI/CD pipeline.

---

## Architecture

GitHub Repository
→ Jenkins Pipeline
→ Docker Build
→ Trivy Security Scan
→ Deploy Candidate Release
→ Health Check Validation
→ Promote Stable Release
→ Rollback on Failure

Application Stack:

* AWS EC2 (Ubuntu 24.04)
* AWS RDS MySQL
* Docker
* Jenkins
* Nginx Reverse Proxy
* Certbot / Let's Encrypt SSL
* GitHub

---

## Features

### Application Features

* Create Tasks
* Update Tasks
* Delete Tasks
* View Tasks
* MySQL Database Integration
* Health Endpoint Validation

Health Endpoint:

```http
GET /health
```

Checks:

* Application availability
* Database connectivity

---

## AWS Infrastructure

### EC2

Ubuntu EC2 instance hosting:

* Jenkins
* Docker Engine
* Flask Application
* Nginx

### RDS

MySQL database configured for persistent application storage.

Security groups configured with least-privilege access.

---

## Docker Implementation

### Dockerfile

Application is containerized using Docker.

### Docker Compose

Used for local development and testing.

### Environment Variables

Configuration managed through:

```text
.env
.env.example
```

Sensitive credentials are excluded from Git.

---

## Jenkins CI/CD Pipeline

### Pipeline Stages

1. Clean Workspace
2. Source Checkout
3. Code Validation
4. Build Candidate Image
5. Security Scan (Trivy)
6. Deploy Candidate Release
7. Verify Application Health
8. Rollback To Stable Release (if required)
9. Promote Release To Stable
10. Cleanup Old Images
11. Docker Housekeeping

---

## Security Scanning

Trivy is used to scan Docker images for:

* Critical vulnerabilities
* High severity vulnerabilities

Pipeline continues while reporting findings for review.

---

## Rollback Strategy

### Successful Deployment

Health check passes:

* Candidate image promoted as Stable image.

### Failed Deployment

Health check fails:

* Candidate container stopped.
* Stable image deployed automatically.
* Service restored using previously validated image.

### First Deployment Failure

If no Stable image exists:

* Deployment marked failed.
* Candidate image retained for troubleshooting.

---

## Image Retention Strategy

Maintained:

* Stable image
* Latest two build images

Automatically removed:

* Older build images

Benefits:

* Reduced disk consumption
* Faster Docker operations
* Cleaner host management

---

## Jenkins Security

### Admin User

Full administrative access.

### Viewer User

Read-only access provided for assessment and review.

Capabilities:

* View jobs
* View logs
* View pipeline execution

Restrictions:

* Cannot modify jobs
* Cannot trigger builds
* Cannot delete resources

---

## AWS IAM Security

Created dedicated IAM read-only reviewer account.

Permissions:

* EC2 Describe
* RDS Describe
* CloudWatch Read

Restrictions:

* No infrastructure modifications
* No resource creation
* No resource deletion

---

## Domain and SSL

Application exposed through Nginx reverse proxy.

SSL certificate generated using:

* Certbot
* Let's Encrypt

Benefits:

* HTTPS encryption
* Secure browser access
* Automatic certificate renewal

---

## Monitoring and Validation

Deployment validation performed through:

```http
GET /health
```

Checks:

* Application running
* Database reachable
* Service healthy

---

## Security Best Practices

* Secrets stored outside source code
* Environment variable based configuration
* Read-only reviewer accounts
* IAM least-privilege permissions
* HTTPS enabled
* Docker image vulnerability scanning

---

## Outcome

Successfully implemented a production-style CI/CD pipeline with automated deployment, health validation, security scanning, rollback capability, access control, and SSL-secured application delivery using AWS, Docker, Jenkins, and Flask.

## Future Enhancements

The current implementation fulfills the project requirements and demonstrates a complete CI/CD workflow. The following enhancements can be implemented in future iterations:

### Container Registry Integration

* Integrate Amazon ECR or Docker Hub.
* Store validated Docker images externally.
* Reduce storage consumption on the EC2 instance.
* Enable easier image version management and rollback.

### Advanced Deployment Strategies

* Blue-Green Deployment
* Canary Deployment
* Zero-Downtime Deployment

### Automated Testing

* Unit Testing using Pytest
* Integration Testing
* Automated API Validation

### Monitoring and Observability

* Prometheus Metrics Collection
* Grafana Dashboards
* CloudWatch Application Monitoring
* Centralized Log Aggregation

### Notification Integration

* Email Notifications
* Slack Notifications
* Microsoft Teams Notifications

### Jenkins Improvements

* Jenkins Agent-Based Builds
* Docker-Based Jenkins Agents
* Parallel Pipeline Execution

### Security Enhancements

* SonarQube Code Quality Analysis
* Secrets Management using AWS Secrets Manager
* Container Image Signing
* Automated Dependency Vulnerability Scanning

### Infrastructure as Code

* Terraform-based Infrastructure Provisioning
* Automated Environment Creation
* Multi-Environment Deployments (Dev, QA, Production)

### Kubernetes Adoption

* Amazon EKS Deployment
* Helm Charts
* Auto Scaling and Self-Healing Workloads

### High Availability

* Application Load Balancer
* Multi-AZ Deployment
* Automated Backup and Disaster Recovery

These enhancements would further improve scalability, security, reliability, and operational efficiency in a production-grade environment.

