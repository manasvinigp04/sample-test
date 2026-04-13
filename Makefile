.PHONY: help install setup seed clean test services gateway user-service product-service health

# Use virtual environment Python
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

help:
	@echo "🛒 E-commerce Microservices - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "Quick Start (First Time):"
	@echo "  make start          - Setup database and start all services"
	@echo ""
	@echo "Quick Start (After First Time):"
	@echo "  make services       - Start all services (DB already exists)"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install        - Install all dependencies"
	@echo "  make setup          - Initialize database and seed data"
	@echo "  make seed           - Seed database with test data"
	@echo ""
	@echo "Running Services:"
	@echo "  make gateway        - Run API Gateway only (port 8000)"
	@echo "  make user-service   - Run User Service only (port 8001)"
	@echo "  make product-service - Run Product Service only (port 8002)"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  make health         - Check health of all services"
	@echo "  make test-auth      - Test authentication flow"
	@echo "  make test-products  - Test product operations"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean database and cache"
	@echo "  make lint           - Run code linting"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	$(PIP) install -q -r requirements.txt
	$(PIP) install -q -r requirements-dev.txt
	@echo "✅ Dependencies installed"

setup: install
	@echo "🔧 Setting up database..."
	PYTHONPATH=. $(PYTHON) scripts/seed_db.py
	@echo "✅ Setup complete!"

seed:
	@echo "🌱 Seeding database..."
	PYTHONPATH=. $(PYTHON) scripts/seed_db.py

clean:
	@echo "🧹 Cleaning up..."
	rm -f ecommerce.db
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Run all services in parallel using & (background processes)
services:
	@echo "🚀 Starting all microservices..."
	@echo "================================="
	@echo ""
	@echo "Starting services in parallel..."
	@PYTHONPATH=. $(PYTHON) src/services/user_service/main.py & \
	PYTHONPATH=. $(PYTHON) src/services/product_service/main.py & \
	sleep 2 && PYTHONPATH=. $(PYTHON) src/gateway/main.py
	@echo ""
	@echo "Press Ctrl+C to stop all services"

# Run services with setup first
start: setup services

gateway:
	@echo "🌐 Starting API Gateway on http://localhost:8000"
	PYTHONPATH=. $(PYTHON) src/gateway/main.py

user-service:
	@echo "👤 Starting User Service on http://localhost:8001"
	PYTHONPATH=. $(PYTHON) src/services/user_service/main.py

product-service:
	@echo "📦 Starting Product Service on http://localhost:8002"
	PYTHONPATH=. $(PYTHON) src/services/product_service/main.py

health:
	@echo "🏥 Checking service health..."
	@echo ""
	@echo "Gateway (8000):"
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Gateway not responding"
	@echo ""
	@echo "User Service (8001):"
	@curl -s http://localhost:8001/health | python -m json.tool || echo "❌ User Service not responding"
	@echo ""
	@echo "Product Service (8002):"
	@curl -s http://localhost:8002/health | python -m json.tool || echo "❌ Product Service not responding"

test-auth:
	@echo "🔐 Testing authentication flow..."
	@echo ""
	@echo "1. Registering new user..."
	@curl -s -X POST http://localhost:8000/api/v1/auth/register \
		-H "Content-Type: application/json" \
		-d '{"email":"test@example.com","username":"testuser","password":"Test1234!","full_name":"Test User"}' \
		| python -m json.tool
	@echo ""
	@echo "2. Logging in..."
	@curl -s -X POST http://localhost:8000/api/v1/auth/login \
		-H "Content-Type: application/json" \
		-d '{"username":"customer","password":"Customer123!"}' \
		| python -m json.tool

test-products:
	@echo "📦 Testing product operations..."
	@echo ""
	@echo "1. Listing all products..."
	@curl -s http://localhost:8000/api/v1/products | python -m json.tool
	@echo ""
	@echo "2. Getting product #1..."
	@curl -s http://localhost:8000/api/v1/products/1 | python -m json.tool
	@echo ""
	@echo "3. Listing categories..."
	@curl -s http://localhost:8000/api/v1/categories | python -m json.tool

lint:
	@echo "🔍 Running linters..."
	@echo "Not configured yet - install ruff/mypy if needed"
