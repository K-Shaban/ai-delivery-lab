# AI Delivery Lab - AWS Validation
#
# Purpose:
# Validate the small set of AWS steps needed to prove that the
# containerised ML API is running on ECS/Fargate.
#
# Run ONE section at a time. This is a learning record, not an
# automated deployment script.

$Region = "ap-southeast-2"
$AccountId = "200978365775"
$Repository = "customer-risk-intelligence-pipeline"
$Cluster = "ai-delivery-lab"
$Service = "ai-delivery-lab"
$LogGroup = "/ecs/ai-delivery-lab"

# ============================================================
# 1. Confirm AWS account
# Why: Make sure the CLI is connected to the expected account.
# ============================================================

aws sts get-caller-identity


# ============================================================
# 2. Confirm ECR repository
# Why: ECR stores the Docker image used by Fargate.
# ============================================================

aws ecr describe-repositories `
  --repository-names $Repository `
  --region $Region


# ============================================================
# 3. Authenticate Docker with ECR
# Why: Allows Docker to push the application image to AWS.
# ============================================================

aws ecr get-login-password `
  --region $Region |
  docker login `
  --username AWS `
  --password-stdin `
  "$AccountId.dkr.ecr.$Region.amazonaws.com"


# ============================================================
# 4. Build and push the application image
# Why: Creates the deployable container and stores it in ECR.
# ============================================================

docker build -t $Repository .

docker tag `
  "${Repository}:latest" `
  "$AccountId.dkr.ecr.$Region.amazonaws.com/${Repository}:latest"

docker push `
  "$AccountId.dkr.ecr.$Region.amazonaws.com/${Repository}:latest"


# ============================================================
# 5. Confirm ECS cluster
# Why: The ECS cluster is where the Fargate service runs.
# ============================================================

aws ecs describe-clusters `
  --clusters $Cluster `
  --region $Region


# ============================================================
# 6. Register the task definition
# Why: Defines the container, model, port, health check,
# CPU/memory, and logging configuration for Fargate.
# ============================================================

aws ecs register-task-definition `
  --cli-input-json file://infrastructure/ecs-task-definition.json `
  --region $Region


# ============================================================
# 7. Confirm ECS service
# Why: The service keeps the required Fargate task running.
# ============================================================

aws ecs describe-services `
  --cluster $Cluster `
  --services $Service `
  --region $Region


# ============================================================
# 8. Find the running task
# Why: Confirms that Fargate actually launched the container.
# ============================================================

aws ecs list-tasks `
  --cluster $Cluster `
  --service-name $Service `
  --region $Region


# ============================================================
# 9. Inspect the task
# Why: Confirms the task is RUNNING and HEALTHY.
#
# Replace <TASK_ID> with the task returned above.
# ============================================================

aws ecs describe-tasks `
  --cluster $Cluster `
  --tasks <TASK_ID> `
  --region $Region


# ============================================================
# 10. Check CloudWatch logs
# Why: Confirms the running container can send application logs.
# ============================================================

aws logs describe-log-streams `
  --log-group-name $LogGroup `
  --region $Region


# ============================================================
# 11. Validate the live API
# Why: Proves the complete path works:
# Internet -> Fargate -> FastAPI -> ML model -> prediction.
#
# Replace <PUBLIC_IP> with the task's public IP.
# ============================================================

curl "http://<PUBLIC_IP>:8000/health"

$Body = @{
  Recency = 30
  Frequency = 5
  TotalQuantity = 100
  MonetaryValue = 500
  AverageOrderValue = 100
  UniqueProducts = 20
  Country = "United Kingdom"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://<PUBLIC_IP>:8000/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body $Body


# ============================================================
# SUCCESS CRITERIA
# ============================================================
#
# The deployment is working when:
#
# - ECR contains the image
# - ECS service has a running task
# - Task health is HEALTHY
# - /health returns {"status":"ok"}
# - /predict returns at_risk and risk_probability
#
# That's enough for the current MVP.
