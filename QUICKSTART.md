# ⚡ Quick Start Guide

## Get Running in 60 Seconds

### Step 1: Setup (First Time Only)
```bash
make setup
```

This will:
- Install all dependencies
- Create SQLite database
- Seed with test data

### Step 2: Start Services
```bash
make services
```

Or use the startup script:
```bash
./start_services.sh
```

### Step 3: Test It!

Open your browser:
- **API Docs:** http://localhost:8000/docs
- **Try the API in Swagger UI** - it's interactive!

Or use curl:
```bash
# Health check
curl http://localhost:8000/health

# List products
curl http://localhost:8000/api/v1/products

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"customer","password":"Customer123!"}'
```

## That's It! 🎉

Your microservices are running!

---

## Next Steps

1. **Explore the API** - Use Swagger UI (http://localhost:8000/docs)
2. **Read the docs** - Check README.md and IMPLEMENTATION_SUMMARY.md
3. **Make changes** - Follow the established patterns

## Test Accounts

- Admin: `admin` / `Admin123!`
- Customer: `customer` / `Customer123!`

## Services Running

- Gateway: http://localhost:8000
- User Service: http://localhost:8001
- Product Service: http://localhost:8002

## Need Help?

```bash
make help          # Show all commands
make health        # Check service health
make test-auth     # Test authentication
make test-products # Test products
```

---

**Everything is working and ready to use!** 🚀
