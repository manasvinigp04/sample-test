# Production-Grade E-commerce Microservices API

A modern, scalable e-commerce platform built with microservices architecture featuring authentication, caching, and proper separation of concerns.

## 🏗️ Architecture

### Microservices

1. **API Gateway** (Port 8000) - Main entry point, routes to all services
2. **User Service** (Port 8001) - Authentication, JWT, user management
3. **Product Service** (Port 8002) - Products, categories, inventory with Redis caching

### Technology Stack

- **Framework:** FastAPI (async Python)
- **Database:** SQLite with SQLAlchemy ORM (async)
- **Cache:** Redis for product caching
- **Auth:** JWT tokens with session management
- **Architecture:** Clean architecture with repository pattern

### Key Features

✅ Microservices architecture with service separation  
✅ JWT authentication with token sessions  
✅ Redis caching for product data  
✅ Repository pattern for data access  
✅ Pydantic validation at all layers  
✅ Comprehensive error handling  
✅ Feature flags for all services  
✅ Health check endpoints  
✅ CORS enabled  
✅ API documentation (Swagger UI)  

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Redis server (optional - caching will be disabled if not available)

### 1. Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and initialize database
make setup
```

This will:
- Install all Python dependencies
- Create SQLite database
- Seed with test data (users, products, categories)

### 2. Start Services

**Option A: All services at once (Recommended)**

```bash
make services
```

This starts:
- User Service on http://localhost:8001
- Product Service on http://localhost:8002
- API Gateway on http://localhost:8000

**Option B: Individual services**

```bash
# Terminal 1: User Service
make user-service

# Terminal 2: Product Service
make product-service

# Terminal 3: Gateway
make gateway
```

### 3. Access the API

- **API Gateway:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 📖 API Endpoints

### Authentication (User Service)

```bash
# Register new user
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "Password123!",
  "full_name": "Full Name"
}

# Login
POST /api/v1/auth/login
{
  "username": "customer",
  "password": "Customer123!"
}
# Returns: { "access_token": "...", "token_type": "bearer", "user": {...} }

# Get current user profile (requires auth)
GET /api/v1/auth/me
Authorization: Bearer <token>

# Update profile
PUT /api/v1/auth/me
Authorization: Bearer <token>
{
  "full_name": "Updated Name"
}

# Logout
POST /api/v1/auth/logout
Authorization: Bearer <token>
```

### Products (Product Service)

```bash
# List all products
GET /api/v1/products

# Filter products
GET /api/v1/products?category=electronics&min_price=50

# Get specific product (cached)
GET /api/v1/products/{id}

# Create product (admin only)
POST /api/v1/products
{
  "name": "Product Name",
  "description": "Description",
  "price": 99.99,
  "stock": 100,
  "category": "electronics"
}

# Update product
PUT /api/v1/products/{id}
{
  "price": 89.99,
  "stock": 150
}

# Delete product
DELETE /api/v1/products/{id}

# List categories
GET /api/v1/categories
```

---

## 🧪 Testing

### Test Authentication Flow

```bash
make test-auth
```

### Test Product Operations

```bash
make test-products
```

### Check Service Health

```bash
make health
```

### Manual Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test1234!","full_name":"Test User"}'

# Login and save token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"customer","password":"Customer123!"}' | jq -r '.access_token')

# Get profile
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# List products
curl http://localhost:8000/api/v1/products

# Get product by ID (test caching)
curl http://localhost:8000/api/v1/products/1
```

---

## 🗄️ Database Schema

### Users Table
- id, email (unique), username (unique), password_hash
- full_name, role (customer/admin), is_active
- created_at, updated_at

### User Sessions Table
- id, user_id, token_jti (JWT ID), expires_at
- Tracks active JWT tokens

### Products Table
- id, name, description, price, stock
- category_id, image_url, is_active
- created_at, updated_at

### Categories Table
- id, name (unique), description, created_at

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Environment
ENV=local  # local, docker, staging, production

# Services
USER_SERVICE_ENABLED=true
PRODUCT_SERVICE_ENABLED=true

# Features
ENABLE_REDIS_CACHE=true
ENABLE_RATE_LIMITING=true
ENABLE_SWAGGER_UI=true

# Database
DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db

# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Logging
LOG_LEVEL=INFO
```

---

## 👥 Test Credentials

Seeded automatically on setup:

**Admin User:**
- Username: `admin`
- Password: `Admin123!`
- Email: admin@example.com

**Customer User:**
- Username: `customer`
- Password: `Customer123!`
- Email: customer@example.com

---

## 📁 Project Structure

```
sample-test/
├── src/
│   ├── common/               # Shared utilities
│   │   ├── auth.py          # JWT & password hashing
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── redis_client.py  # Redis caching
│   │   ├── exceptions.py    # Custom exceptions
│   │   ├── validators.py    # Shared validators
│   │   └── constants.py     # Service URLs, enums
│   │
│   ├── gateway/             # API Gateway
│   │   └── main.py         # Routes to services
│   │
│   └── services/
│       ├── user_service/    # Port 8001
│       │   ├── models/     # Database & Pydantic models
│       │   ├── services/   # Business logic
│       │   ├── api/        # Routes & dependencies
│       │   ├── repository.py
│       │   └── main.py
│       │
│       └── product_service/ # Port 8002
│           ├── models/
│           ├── services/
│           ├── api/
│           ├── repository.py
│           ├── cache.py    # Redis caching
│           └── main.py
│
├── scripts/
│   └── seed_db.py          # Database seeding
│
├── Makefile                # Build commands
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## 🔍 Key Design Patterns

### Repository Pattern
Separates data access from business logic:
- `repository.py` - Database operations
- `services/` - Business logic
- `api/routes.py` - HTTP endpoints

### Service Layer
Each service is self-contained with:
- Database models (SQLAlchemy)
- API models (Pydantic)
- Business logic (Services)
- HTTP routes (FastAPI)

### Caching Strategy
Product Service uses Redis caching:
- Cache on read (get product by ID)
- Invalidate on write (update/delete)
- TTL: 5 minutes (configurable)
- Falls back gracefully if Redis unavailable

### Authentication Flow
1. User logs in → receives JWT token
2. Token includes: user_id, username, role, expiry, JTI
3. Session stored in database with JTI
4. Each request validates token + checks session exists
5. Logout deletes session → token becomes invalid

---

## 🛠️ Development

### Adding a New Service

1. Create service directory: `src/services/your_service/`
2. Add models, repository, services, api
3. Create `main.py` with FastAPI app
4. Add service URL to `src/common/constants.py`
5. Add routes to gateway in `src/gateway/main.py`

### Running Without Gateway

Services can run independently:

```bash
# Access services directly
curl http://localhost:8001/health  # User Service
curl http://localhost:8002/health  # Product Service
```

---

## 📊 Comparison: Before vs After

### Before (Original)
- ❌ Single file (166 lines)
- ❌ In-memory storage
- ❌ No authentication
- ❌ No caching
- ❌ No service separation
- ❌ Intentional validation issues

### After (Current)
- ✅ Microservices architecture
- ✅ SQLite database (persistent)
- ✅ JWT authentication
- ✅ Redis caching
- ✅ 4 separate services
- ✅ Full validation at all layers
- ✅ Production-ready patterns
- ✅ Comprehensive error handling
- ✅ Feature flags
- ✅ Health checks

---

## 🐛 Troubleshooting

### Services won't start

```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8001
lsof -i :8002

# Clean and restart
make clean
make setup
make services
```

### Redis connection errors

Redis is optional - if unavailable, caching will be disabled automatically. Install Redis:

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
```

### Database errors

```bash
# Reset database
make clean
make setup
```

---

## 📝 TODO / Future Enhancements

- [ ] Order Service (cart, checkout)
- [ ] Payment Service (Stripe integration)
- [ ] Docker Compose configuration
- [ ] Kubernetes manifests
- [ ] Rate limiting middleware
- [ ] API versioning
- [ ] Unit tests (pytest)
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Message queue (RabbitMQ/Celery)
- [ ] Search (Elasticsearch)

---

## 📄 License

MIT License - Feel free to use for learning and projects.

---

## 🙋 Support

For issues or questions:
1. Check service health: `make health`
2. View logs in terminal
3. Check Swagger docs: http://localhost:8000/docs
