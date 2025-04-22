## Week 2: Deploy the URL Shortener using Kubernetes

This folder contains the Kubernetes configuration files for deploying the URL shortener application.

## File Structure

```
week2/
├── k8s/
│   ├── url-shortener-deployment.yaml  # URL shortener pod configuration
│   ├── url-shortener-service.yaml     # Service to expose URL shortener
│   ├── redis-deployment.yaml          # Redis pod configuration
│   ├── redis-service.yaml             # ClusterIP service for Redis
│   ├── configmap.yaml                 # Configuration values
│   └── secret.yaml                    # Sensitive configuration
└── README.md                          # Documentation
```

## How to run

1. Navigate to week1 directory first
cd ../week1


2. Build and load the URL shortener Docker image to your cluster:
   
   eval $(minikube docker-env)
   docker build -t url-shortener:latest ./app

# Navigate back to week2 to continue with Kubernetes deployment
cd ../week2

3. Apply the Redis deployment and service:
   
   kubectl apply -f k8s/redis-deployment.yaml
   kubectl apply -f k8s/redis-service.yaml
   

4. Apply the ConfigMap and Secret:
   
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml

5. Apply the URL shortener deployment and service:
  
   kubectl apply -f k8s/url-shortener-deployment.yaml
   kubectl apply -f k8s/url-shortener-service.yaml
  

6. Check the deployment status:
  
   kubectl get pods
   kubectl get services
   

7. Test the service:
   
   
   minikube service url-shortener-service --url

   ## To test your URL shortener from your Ubuntu terminal

   curl -X POST http://127.0.0.1:35487/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
