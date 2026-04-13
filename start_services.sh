#!/bin/bash

# Startup script for E-commerce Microservices

echo "🚀 Starting E-commerce Microservices"
echo "======================================"
echo ""

# Set PYTHONPATH
export PYTHONPATH=/Users/I764709/sample-test

# Activate virtual environment
source .venv/bin/activate

# Check if database exists
if [ ! -f "ecommerce.db" ]; then
    echo "📦 Database not found. Running setup..."
    python scripts/seed_db.py
    echo ""
fi

echo "Starting services..."
echo ""

# Start services in background
echo "👤 User Service starting on port 8001..."
python src/services/user_service/main.py > /dev/null 2>&1 &
USER_PID=$!

sleep 1

echo "📦 Product Service starting on port 8002..."
python src/services/product_service/main.py > /dev/null 2>&1 &
PRODUCT_PID=$!

sleep 2

echo "🌐 API Gateway starting on port 8000..."
python src/gateway/main.py &
GATEWAY_PID=$!

echo ""
echo "✅ All services started!"
echo ""
echo "📍 API Gateway: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🏥 Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for gateway process
wait $GATEWAY_PID

# Cleanup on exit
echo ""
echo "🛑 Stopping all services..."
kill $USER_PID $PRODUCT_PID 2>/dev/null
echo "✅ All services stopped"
