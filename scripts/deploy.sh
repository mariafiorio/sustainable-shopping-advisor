#!/bin/bash
# Deploy Sustainable Shopping Advisor to Kubernetes

set -e

echo "🚀 Deploying Sustainable Shopping Advisor - Agentic AI Extension"
echo "=================================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster connection verified"

# Deploy Online Boutique (if not already deployed)
echo "🛍️ Checking for Online Boutique deployment..."
if ! kubectl get deployment frontend &> /dev/null; then
    echo "📦 Deploying Online Boutique as base platform..."
    kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/main/release/kubernetes-manifests.yaml
    
    echo "⏳ Waiting for Online Boutique to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/frontend
    echo "✅ Online Boutique deployed successfully"
else
    echo "✅ Online Boutique already deployed"
fi

# Deploy Agentic AI Extension
echo "🧠 Deploying Agentic AI Extension..."

# Apply ConfigMaps first
echo "📋 Creating ConfigMaps..."
kubectl apply -f k8s/k8s-sustainable-advisor-configmap.yaml
kubectl apply -f k8s/k8s-recommender-agent-configmap.yaml
kubectl apply -f k8s/k8s-widget-configmap.yaml

# Apply Deployments and Services
echo "🚀 Creating Deployments and Services..."
kubectl apply -f k8s/k8s-sustainable-advisor.yaml
kubectl apply -f k8s/k8s-recommender-agent.yaml
kubectl apply -f k8s/k8s-widget-server.yaml

echo "⏳ Waiting for Agentic AI components to be ready..."

# Wait for deployments to be available
kubectl wait --for=condition=available --timeout=300s deployment/sustainable-advisor
kubectl wait --for=condition=available --timeout=300s deployment/recommender-agent
kubectl wait --for=condition=available --timeout=300s deployment/widget-server

echo "✅ All deployments are ready!"

# Get external IPs
echo "🌐 Getting external URLs..."
echo "=================================================="

echo "📊 Getting service information..."
kubectl get services -l component=agentic-ai -o wide

echo ""
echo "🎯 External URLs (may take a few minutes to provision):"
echo "=================================================="

# Function to get external IP
get_external_ip() {
    local service_name=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        external_ip=$(kubectl get service $service_name -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
        if [ -n "$external_ip" ] && [ "$external_ip" != "null" ]; then
            echo "$external_ip"
            return 0
        fi
        echo "⏳ Waiting for $service_name external IP... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    echo "pending"
    return 1
}

# Get URLs for each service
ADVISOR_IP=$(get_external_ip "sustainable-advisor-external")
RECOMMENDER_IP=$(get_external_ip "recommender-agent-external")
WIDGET_IP=$(get_external_ip "widget-server-external")
BOUTIQUE_IP=$(get_external_ip "frontend-external")

echo "🌱 Sustainable Advisor API: http://$ADVISOR_IP"
echo "🎯 Recommender Agent API: http://$RECOMMENDER_IP"
echo "🖱️ Widget Demo: http://$WIDGET_IP"
echo "🛍️ Online Boutique (with AI): http://$BOUTIQUE_IP"

echo ""
echo "🧪 Testing deployment..."
echo "=================================================="

# Test health endpoints
if [ "$ADVISOR_IP" != "pending" ]; then
    echo "🩺 Testing Sustainable Advisor health..."
    if curl -f http://$ADVISOR_IP/health &>/dev/null; then
        echo "✅ Sustainable Advisor is healthy"
    else
        echo "⚠️ Sustainable Advisor health check failed (may still be starting)"
    fi
fi

if [ "$RECOMMENDER_IP" != "pending" ]; then
    echo "🩺 Testing Recommender Agent health..."
    if curl -f http://$RECOMMENDER_IP/health &>/dev/null; then
        echo "✅ Recommender Agent is healthy"
    else
        echo "⚠️ Recommender Agent health check failed (may still be starting)"
    fi
fi

echo ""
echo "🎉 Deployment Complete!"
echo "=================================================="
echo "🚀 Your Agentic AI Extension is now running!"
echo ""
echo "📋 Next Steps:"
echo "1. Visit the Widget Demo: http://$WIDGET_IP"
echo "2. Drag the bookmarklet to your bookmarks bar"
echo "3. Go to the Online Boutique: http://$BOUTIQUE_IP"
echo "4. Click the bookmarklet to see Agentic AI in action!"
echo ""
echo "📊 Monitor your deployment:"
echo "kubectl get pods -l component=agentic-ai"
echo "kubectl logs -l app=sustainable-advisor --tail=100"
echo ""
echo "🎯 API Documentation available in README.md"
echo "=================================================="