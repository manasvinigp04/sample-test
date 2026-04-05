# Sample E-commerce API - ACV Test Project

A realistic e-commerce API to test the API Contract Validator library.

## Features

- User management
- Product catalog
- Shopping cart
- Order processing
- Intentional drift issues for testing ACV

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (includes ACV)
pip install -r requirements.txt

# Verify ACV
acv --version
```

## Quick Test

```bash
# Terminal 1: Start API
python src/api/main.py

# Terminal 2: Run ACV validation
acv validate
```

## Expected ACV Results

This API has **intentional issues** to test ACV:

- ✅ Contract drift detection
- ✅ Validation drift (weak input validation)
- ✅ Boundary test failures
- ✅ Multi-endpoint validation

## Testing ACV Changes

Make changes to ACV and test immediately:

```bash
cd /Users/I764709/api-contract-validator
# Edit any file

cd ~/sample-test
acv validate  # Uses latest ACV code!
```

No reinstall needed!
