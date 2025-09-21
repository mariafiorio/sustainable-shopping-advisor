#!/bin/bash
# Test Sustainable Shopping Advisor locally

set -e

echo "🧪 Testing Sustainable Shopping Advisor - Local Development"
echo "=================================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r src/sustainable-advisor/requirements.txt
pip install -q -r src/recommender-agent/requirements.txt

echo "✅ Dependencies installed"

# Start services in background
echo "🚀 Starting Agentic AI services..."

# Kill any existing processes
pkill -f "python.*api.py" || true
pkill -f "python.*app.py" || true

# Start Sustainable Advisor
echo "🌱 Starting Sustainable Advisor on port 5002..."
cd src/sustainable-advisor
python api.py &
ADVISOR_PID=$!
cd ../..

# Wait a moment for startup
sleep 2

# Start Recommender Agent
echo "🎯 Starting Recommender Agent on port 5001..."
cd src/recommender-agent
python app.py &
RECOMMENDER_PID=$!
cd ../..

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 5

# Test health endpoints
echo "🩺 Testing service health..."

# Test Sustainable Advisor
if curl -f http://localhost:5002/health &>/dev/null; then
    echo "✅ Sustainable Advisor is healthy (port 5002)"
else
    echo "❌ Sustainable Advisor health check failed"
    exit 1
fi

# Test Recommender Agent
if curl -f http://localhost:5001/health &>/dev/null; then
    echo "✅ Recommender Agent is healthy (port 5001)"
else
    echo "❌ Recommender Agent health check failed"
    exit 1
fi

# Test API functionality
echo "🧪 Testing API functionality..."

# Test recommendations endpoint
echo "🔍 Testing recommendations..."
RECOMMENDATIONS=$(curl -s http://localhost:5002/recommendations?query=bottle)
if echo "$RECOMMENDATIONS" | grep -q "sustainability_score"; then
    echo "✅ Recommendations API working"
else
    echo "❌ Recommendations API failed"
fi

# Test A2A communication
echo "🤝 Testing Agent-to-Agent communication..."
A2A_TEST=$(curl -s -X POST http://localhost:5001/rank \
  -H "Content-Type: application/json" \
  -d '{"products": [{"name": "test", "price": 10}], "preferences": {"sustainability": 0.8}}')
if echo "$A2A_TEST" | grep -q "ranked_products"; then
    echo "✅ A2A communication working"
else
    echo "❌ A2A communication failed"
fi

echo ""
echo "🎉 Local Testing Complete!"
echo "=================================================="
echo "✅ All services are running successfully!"
echo ""
echo "📊 Service URLs:"
echo "🌱 Sustainable Advisor: http://localhost:5002"
echo "🎯 Recommender Agent: http://localhost:5001"
echo ""
echo "🔍 API Endpoints to test:"
echo "curl http://localhost:5002/health"
echo "curl http://localhost:5002/recommendations?query=bottle"
echo "curl http://localhost:5001/health"
echo "curl -X POST http://localhost:5001/rank -H 'Content-Type: application/json' -d '{\"products\": [{\"name\": \"test\"}]}'"
echo ""
echo "🛑 To stop services:"
echo "kill $ADVISOR_PID $RECOMMENDER_PID"
echo ""
echo "📚 Next: Run './scripts/deploy.sh' to deploy to Kubernetes"
echo "=================================================="

# Keep services running
echo "🔄 Services are running. Press Ctrl+C to stop."
wait