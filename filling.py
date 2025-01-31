import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bd_3 import Base, User, Product, Category

fake = Faker

# Создание соединение с базой
engine = create_engine("sqlite:///test2.bd")
SessionLocal = sessionmaker(bind=engine)


def filling_bd():
    with SessionLocal() as session:
        categories = ["Electron", "Textile", "Furniture", "Toys"]
        for category_name in categories:
            category = Category(name=category_name)
            session.add(category)
        session.commit()

        # Добовляем пользователей
        for _ in range(10):
            user = User(
                user_id=random.randint(1, 1000),
                name=fake.name(),
                phone=fake.phone_number(),
            )
            session.add(user)
        session.commit()

        # Добаляем продукты
        product_names = ["Smartphone", "Laptop", "T-Shirt", "Coffee Table", "Doll"]
        for _ in range(20):
            product = Product(
                name=random.choice(product_names),
                description=fake.sentence(),
                price=random.randint(0, 100),
                category_id=random.randint(1, len(categories)),
            )
            session.add(product)
        session.commit()
    print("База данных  заполнена тестовыми данными.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    filling_bd()
