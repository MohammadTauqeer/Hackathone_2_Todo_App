# Quickstart Guide: Phase V - Advanced Cloud Deployment

## Overview
This guide provides instructions for setting up, running, and deploying the Phase V Cloud Native Todo Chatbot with advanced features, event-driven architecture, and Dapr integration.

## Prerequisites

### Local Development
- Docker Desktop (with Kubernetes enabled)
- Minikube
- kubectl
- Helm 3
- Python 3.11+
- Node.js 18+
- Dapr CLI
- Java 11+ (for Kafka if running locally)

### Cloud Deployment
- Cloud account (Oracle OCI, Microsoft Azure, or Google Cloud)
- Cloud CLI tools (oci, az, or gcloud)
- GitHub account for CI/CD

## Local Setup

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dapr
```bash
# Using Dapr CLI
dapr init

# Or using Helm for Kubernetes
kubectl create namespace dapr-system
helm repo add dapr https://daprio.azurecr.io/
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --set global.logAsJson=true
```

### 3. Start Local Kafka/Redpanda
```bash
# Option 1: Using Docker Compose (if available)
docker-compose -f docker/local-kafka.yml up -d

# Option 2: Using Redpanda Helm chart
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm install redpanda redpanda/redpanda --namespace redpanda --create-namespace
```

### 4. Set Up Backend
```bash
cd backend
pip install -r requirements.txt

# Run with Dapr
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python src/main.py
```

### 5. Set Up Frontend
```bash
cd frontend
npm install
npm run dev
```

## Running Locally with Minikube

### 1. Start Minikube
```bash
minikube start --memory=8192 --cpus=4
minikube addons enable ingress
```

### 2. Install Dapr on Minikube
```bash
dapr init -k
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr-operator --namespace=dapr-system
```

### 3. Deploy Kafka/Redpanda
```bash
kubectl create namespace messaging
helm install kafka redpanda/redpanda --namespace messaging --set resources.memory.requests=2Gi
```

### 4. Build and Push Images
```bash
# Set Docker env to Minikube
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:latest -f backend/Dockerfile .
docker build -t todo-frontend:latest -f frontend/Dockerfile .

# Verify images
docker images | grep todo
```

### 5. Deploy Application
```bash
cd k8s/helm-charts
helm install todo-chatbot . --namespace todo-app --create-namespace
```

### 6. Access Application
```bash
# Get Minikube IP
minikube ip

# Port forward if needed
kubectl port-forward svc/todo-frontend 8080:80 --namespace todo-app
```

## Cloud Deployment

### 1. Choose Cloud Provider
Select one of the following based on free tier availability:

#### Oracle Cloud Infrastructure (Recommended for Free Tier)
```bash
# Login to OCI
oci auth login

# Create free tier eligible cluster
oci ce cluster create --name todo-cluster --vcn-id <vcn-id> --subnet-ids <subnet-id>
```

#### Azure Kubernetes Service
```bash
# Login to Azure
az login

# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create --resource-group todo-rg --name todo-cluster --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

#### Google Kubernetes Engine
```bash
# Login to Google Cloud
gcloud auth login

# Set project
gcloud config set project <project-id>

# Create GKE cluster
gcloud container clusters create todo-cluster --num-nodes=1 --zone=us-central1-a
```

### 2. Configure kubectl
```bash
# For AKS
az aks get-credentials --resource-group todo-rg --name todo-cluster

# For GKE
gcloud container clusters get-credentials todo-cluster --zone=us-central1-a --project <project-id>

# For OKE, follow OCI CLI instructions to get kubeconfig
```

### 3. Install Dapr on Cloud Cluster
```bash
dapr init -k
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=dapr-operator --namespace=dapr-system
```

### 4. Deploy to Cloud
```bash
# Update image registry in Helm values
# Push images to cloud registry (ACR, GCR, OCIR)

# Deploy using Helm
helm upgrade --install todo-chatbot ./k8s/helm-charts --namespace todo-app --create-namespace --set image.registry=<cloud-registry>
```

## CI/CD Setup

### 1. Configure GitHub Secrets
Add the following secrets to your GitHub repository:
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token
- Cloud-specific credentials (e.g., `AZURE_CREDENTIALS`, `OCI_CONFIG`, `GCLOUD_SERVICE_KEY`)

### 2. Enable GitHub Actions
Workflow file is located at `.github/workflows/ci-cd.yaml` and will automatically trigger on pushes to main branch.

## Verification

### 1. Check Running Pods
```bash
kubectl get pods --namespace todo-app
```

### 2. Verify Dapr Sidecars
```bash
kubectl get pods --namespace todo-app -o jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.name},{end}{end}'
```

### 3. Test Application Endpoints
```bash
# Check backend health
curl http://<minikube-ip>:<port>/healthz

# Check frontend
open http://<minikube-ip>:<port>
```

### 4. Verify Event Processing
```bash
# Check Kafka topics
kubectl exec -it -n messaging <kafka-pod> -- kafka-topics --bootstrap-server localhost:9092 --list

# Check Dapr pub/sub
dapr logs -k | grep pubsub
```

## Troubleshooting

### Common Issues
1. **Dapr Sidecar Not Injected**: Ensure namespace has `dapr.io/enabled=true` annotation
2. **Kafka Connection Issues**: Verify Kafka service is running and accessible
3. **Image Pull Errors**: Check image registry configuration and credentials
4. **Resource Limits**: Increase resource requests/limits if pods are being evicted

### Useful Commands
```bash
# View Dapr logs
dapr logs -k

# Check Dapr components
kubectl get components.dapr.io -A

# Check Dapr subscriptions
kubectl get subscriptions.dapr.io -A

# Debug a specific pod
kubectl describe pod <pod-name> -n <namespace>
```

## Next Steps
1. Explore the advanced features: priorities, tags, recurring tasks, due dates
2. Customize the event-driven architecture for your specific use cases
3. Enhance monitoring and observability configurations
4. Scale the application based on your requirements