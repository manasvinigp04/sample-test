"""
E-commerce API - Sample for testing ACV
Run with: python src/api/main.py

This API has intentional issues to test ACV drift detection:
- Weak validation (accepts invalid data)
- Schema mismatches
- Boundary condition failures
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="E-commerce API", version="1.0.0")

# In-memory databases
products_db = [
    {"id": 1, "name": "Laptop", "description": "Gaming laptop", "price": 999.99, "stock": 10, "category": "electronics"},
    {"id": 2, "name": "T-Shirt", "description": "Cotton t-shirt", "price": 19.99, "stock": 50, "category": "clothing"},
    {"id": 3, "name": "Python Book", "description": "Learn Python", "price": 39.99, "stock": 25, "category": "books"},
]
cart_items = []
orders_db = []
next_product_id = 4
next_order_id = 1

# Models
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None

class Product(ProductCreate):
    id: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

# Routes
@app.get("/products")
def list_products(category: Optional[str] = None, min_price: Optional[float] = None):
    """List products with optional filters"""
    result = products_db.copy()

    if category:
        result = [p for p in result if p.get("category") == category]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    return result

@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    """Create product - INTENTIONAL: Weak validation for ACV testing"""
    global next_product_id

    # ISSUE: Not validating name length (spec says minLength: 1, maxLength: 200)
    # ISSUE: Not validating price range (spec says minimum: 0, maximum: 1000000)
    # ISSUE: Not validating stock minimum (spec says minimum: 0)

    new_product = {
        "id": next_product_id,
        **product.model_dump()
    }
    products_db.append(new_product)
    next_product_id += 1

    # ISSUE: Sometimes returns wrong schema structure for testing
    if next_product_id % 10 == 0:
        return {"product_id": new_product["id"], "message": "created"}  # Wrong schema!

    return new_product

@app.get("/products/{productId}")
def get_product(productId: int):
    """Get product by ID"""
    product = next((p for p in products_db if p["id"] == productId), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/cart")
def get_cart():
    """Get cart"""
    total = sum(
        next((p["price"] for p in products_db if p["id"] == item["product_id"]), 0) * item["quantity"]
        for item in cart_items
    )

    return {
        "items": cart_items,
        "total": total
    }

@app.post("/cart")
def add_to_cart(item: CartItem):
    """Add to cart - INTENTIONAL: Weak validation"""
    # ISSUE: Not checking if product exists
    # ISSUE: Not checking stock availability
    # ISSUE: Not validating quantity range (spec says minimum: 1, maximum: 100)

    cart_items.append(item.model_dump())

    total = sum(
        next((p["price"] for p in products_db if p["id"] == ci["product_id"]), 0) * ci["quantity"]
        for ci in cart_items
    )

    return {
        "items": cart_items,
        "total": total
    }

@app.post("/orders", status_code=201)
def create_order(shipping_address: str, notes: Optional[str] = None):
    """Create order - INTENTIONAL: Validation issues"""
    global next_order_id

    # ISSUE: Not validating shipping_address length (spec says minLength: 10, maxLength: 500)
    # ISSUE: Not checking if cart is empty

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(
        next((p["price"] for p in products_db if p["id"] == item["product_id"]), 0) * item["quantity"]
        for item in cart_items
    )

    order = {
        "id": next_order_id,
        "items": cart_items.copy(),
        "total": total,
        "status": "pending",
        "shipping_address": shipping_address
    }

    orders_db.append(order)
    next_order_id += 1
    cart_items.clear()

    return order

@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy", "products": len(products_db), "orders": len(orders_db)}

if __name__ == "__main__":
    import uvicorn
    print("\n🛒 E-commerce API for ACV Testing")
    print("=" * 50)
    print("📍 Server: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("🔍 Health: http://localhost:8000/health")
    print("\n⚠️  This API has intentional issues for ACV testing:")
    print("   - Weak input validation")
    print("   - Schema mismatches")
    print("   - Boundary condition failures")
    print("\n🛑 Press Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
