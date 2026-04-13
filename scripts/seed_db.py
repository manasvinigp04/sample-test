"""Database initialization and seeding script."""
import asyncio
from datetime import datetime

from src.common.database import init_db, AsyncSessionLocal
from src.services.user_service.models.database import User, UserSession
from src.services.product_service.models.database import Product, Category
from src.common.auth import hash_password


async def seed_database():
    """Seed the database with initial data."""
    print("🌱 Seeding database...")

    async with AsyncSessionLocal() as session:
        try:
            # Create categories
            categories_data = [
                {"name": "electronics", "description": "Electronic devices and accessories"},
                {"name": "clothing", "description": "Apparel and fashion items"},
                {"name": "books", "description": "Books and publications"},
                {"name": "home", "description": "Home and garden items"},
            ]

            categories = {}
            for cat_data in categories_data:
                category = Category(**cat_data)
                session.add(category)
                await session.flush()
                categories[cat_data["name"]] = category.id

            # Create users
            users_data = [
                {
                    "email": "admin@example.com",
                    "username": "admin",
                    "password_hash": hash_password("Admin123!"),
                    "full_name": "Admin User",
                    "role": "admin",
                },
                {
                    "email": "customer@example.com",
                    "username": "customer",
                    "password_hash": hash_password("Customer123!"),
                    "full_name": "Test Customer",
                    "role": "customer",
                },
            ]

            for user_data in users_data:
                user = User(**user_data)
                session.add(user)

            await session.flush()

            # Create products
            products_data = [
                {
                    "name": "Gaming Laptop",
                    "description": "High-performance laptop for gaming",
                    "price": 1299.99,
                    "stock": 10,
                    "category_id": categories["electronics"],
                },
                {
                    "name": "Wireless Mouse",
                    "description": "Ergonomic wireless mouse",
                    "price": 29.99,
                    "stock": 50,
                    "category_id": categories["electronics"],
                },
                {
                    "name": "Cotton T-Shirt",
                    "description": "Comfortable cotton t-shirt",
                    "price": 19.99,
                    "stock": 100,
                    "category_id": categories["clothing"],
                },
                {
                    "name": "Python Programming Book",
                    "description": "Learn Python programming",
                    "price": 39.99,
                    "stock": 25,
                    "category_id": categories["books"],
                },
                {
                    "name": "Coffee Maker",
                    "description": "Automatic drip coffee maker",
                    "price": 79.99,
                    "stock": 15,
                    "category_id": categories["home"],
                },
            ]

            for product_data in products_data:
                product = Product(**product_data)
                session.add(product)

            await session.commit()
            print("✅ Database seeded successfully!")
            print("\n📝 Test Credentials:")
            print("   Admin: admin / Admin123!")
            print("   Customer: customer / Customer123!")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise


async def main():
    """Initialize database and seed data."""
    print("🔧 Initializing database...")
    await init_db()
    print("✅ Database initialized")

    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
