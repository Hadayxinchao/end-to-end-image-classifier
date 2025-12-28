#!/bin/bash
# Deploy to Kubernetes cluster

set -e

NAMESPACE="mlops-image-classifier"
IMAGE_NAME="your-registry/image-classifier"
IMAGE_TAG="${1:-latest}"

echo "🚀 Deploying Image Classifier to Kubernetes..."
echo "Namespace: $NAMESPACE"
echo "Image: $IMAGE_NAME:$IMAGE_TAG"

# Create namespace if it doesn't exist
echo ""
echo "📦 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Apply ConfigMaps and Secrets
echo ""
echo "⚙️  Applying ConfigMaps and Secrets..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Create PVC for models
echo ""
echo "💾 Creating Persistent Volume Claims..."
kubectl apply -f k8s/pvc.yaml

# Deploy the application
echo ""
echo "🚢 Deploying application..."
kubectl apply -f k8s/deployment.yaml

# Create service
echo ""
echo "🌐 Creating service..."
kubectl apply -f k8s/service.yaml

# Apply HPA
echo ""
echo "📊 Setting up autoscaling..."
kubectl apply -f k8s/hpa.yaml

# Apply Ingress (optional)
if [ -f "k8s/ingress.yaml" ]; then
    echo ""
    echo "🔗 Setting up ingress..."
    kubectl apply -f k8s/ingress.yaml
fi

# Wait for deployment to be ready
echo ""
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/image-classifier -n $NAMESPACE

# Get deployment status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Deployment status:"
kubectl get deployments -n $NAMESPACE
echo ""
echo "🔍 Pods:"
kubectl get pods -n $NAMESPACE
echo ""
echo "🌐 Services:"
kubectl get services -n $NAMESPACE
echo ""
echo "📈 HPA status:"
kubectl get hpa -n $NAMESPACE

# Get service endpoint
echo ""
echo "🔗 Service endpoint:"
kubectl get service image-classifier-service -n $NAMESPACE

echo ""
echo "🎉 Deployment successful!"
echo ""
echo "To check logs: kubectl logs -f deployment/image-classifier -n $NAMESPACE"
echo "To port-forward: kubectl port-forward service/image-classifier-service 8000:80 -n $NAMESPACE"
