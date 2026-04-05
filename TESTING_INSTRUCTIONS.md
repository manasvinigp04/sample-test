# Testing Instructions

## Setup

```bash
cd ~/sample-test

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (includes ACV)
pip install -r requirements.txt

# Verify
acv --version
```

## Test Scenarios

### Test 1: Basic Validation

**Start API:**
```bash
python src/api/main.py
```

**Run ACV (in another terminal):**
```bash
acv validate
```

**Expected Results:**
- ✅ Parses 5 endpoints
- ✅ Generates ~100+ test cases
- ✅ **Detects validation drift** (API accepts invalid data)
- ✅ **Detects boundary failures** (negative prices, huge quantities)
- ✅ Generates reports in `reports/acv/`

### Test 2: View Drift Issues

```bash
cat reports/acv/drift_report_*.md
```

You should see:
- Validation drift on `/products` POST (accepts invalid prices, names)
- Validation drift on `/cart` POST (accepts invalid quantities)
- Validation drift on `/orders` POST (accepts short addresses)

### Test 3: Parse Spec Only

```bash
acv parse api/openapi.yaml
```

Shows the API structure without running tests.

### Test 4: Generate Tests

```bash
acv generate-tests api/openapi.yaml -o tests/generated_tests.json
cat tests/generated_tests.json | jq '.total_tests'
```

### Test 5: Test ACV Changes

This is the **key feature**!

**Make changes to ACV:**
```bash
cd /Users/I764709/api-contract-validator
vim src/api_contract_validator/analysis/drift/validation_drift.py
# Make your changes
```

**Test immediately:**
```bash
cd ~/sample-test
acv validate  # Uses latest code automatically!
```

No reinstall needed because of `-e` flag in requirements.txt!

### Test 6: Custom Settings

```bash
# More workers
acv validate --parallel 20

# Different output
acv validate --output ./my-reports

# No AI analysis
acv validate --no-ai-analysis
```

## What ACV Will Find

This API has **intentional issues**:

1. **POST /products**
   - Accepts empty names (spec requires minLength: 1)
   - Accepts negative prices (spec requires minimum: 0)
   - Accepts prices > 1000000 (spec maximum: 1000000)
   - Sometimes returns wrong schema structure

2. **POST /cart**
   - Doesn't validate product_id exists
   - Accepts quantity > 100 (spec maximum: 100)
   - Accepts quantity = 0 (spec minimum: 1)

3. **POST /orders**
   - Accepts addresses < 10 chars (spec minLength: 10)
   - Accepts addresses > 500 chars (spec maxLength: 500)

## Expected ACV Output

```
✓ Parsed 5 endpoints
✓ Generated 120 test cases
✓ Executed 120 tests: 85 passed, 35 failed
✓ Detected 15 drift issues
  - 12 validation drift issues
  - 2 contract drift issues  
  - 1 behavioral drift issue

⚠ Drift issues detected - review recommended
```

## Cleanup

```bash
# Stop API
pkill -f "python src/api/main.py"

# Clean reports
rm -rf reports/
```

## Iterative Testing

1. Run `acv validate` - see issues
2. Fix one issue in `src/api/main.py`
3. Run `acv validate` again - fewer issues
4. Or: Modify ACV code and test immediately

This workflow tests ACV as a **reusable library with live updates**!
