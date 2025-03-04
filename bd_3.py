from sqlalchemy import create_engine, Column, Integer, String, Text, REAL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session, relationship


Base = declarative_base()
engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(REAL, nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    img = Column(String)
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    products = relationship("Product", back_populates="category")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(REAL, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


Base.metadata.create_all(engine)


def add_user(user_id: int, name: str, phone: str):
    with SessionLocal() as session:
        new_user = User(user_id=user_id, name=name, phone=phone)
        session.add(new_user)
        session.commit()

    print(f"Добавлен пользователь: {name},телефон:{phone}")


def add_category(name: str):
    with SessionLocal() as session:
        new_category = Category(name=name)
        session.add(new_category)
        session.commit()

    print(f"Добавлена категоря:{name}")


def add_product(
    name: str, description: str, price: float, stock: int, category_id: int
):
    with SessionLocal() as session:
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
        )
    session.add(new_product)
    session.commit()

    print(f"Добавлен продукт: {name}, категория ID: {category_id}")


# Фильтр по всем категориям
def get_all_users():
    with SessionLocal() as session:
        users = session.query(User).all()
        return users


def get_all_categories():
    with SessionLocal() as session:
        categories = session.query(Category).all()
        return categories


def get_all_products():
    with SessionLocal() as session:
        products = session.query(Product).all()
        return products


# Фильтр по имени
def get_user_by_name(name: str):
    with SessionLocal() as session:
        user = session.query(User).filter(User.name == name).all()
        return user


def get_category_by_name(name: str):
    with SessionLocal() as session:
        category = session.query(Category).filter(Category.name == name).all()
        return category


def get_product_by_name(name: str):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.name == name).all()
        return product


if __name__ == "__main__":
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    add_user("Bob", "+723-456-7890")
    add_user("Alex", "+855-465-5457")
    add_category("Electron")
    add_category("Textile")
    add_product("Smartphone", "new model", 699.99, 50, 1)
    add_product("Knitwear", "white", 123, 22, "Textile")
    add_product("Knitwear", "white", 123, 22, "Textile")

    # Получение всех пользователей
users = get_all_users()
print("Все пользователи:")
for user in users:
    print(f"ID: {user.id}, Имя: {user.name}, Телефон: {user.phone}")

# Получение всех категорий
categories = get_all_categories()
print("\nВсе категории:")
for category in categories:
    print(f"ID: {category.id}, Имя: {category.name}")

# Получение всех продуктов
products = get_all_products()
print("\nВсе продукты:")
for product in products:
    print(
        f"ID: {product.id}, Имя: {product.name}, Цена: {product.price}, Запас: {product.stock}, Категория ID: {product.category_id}"
    )


# Получение пользователя по имени
found_users = get_user_by_name("Bob")
print("\nНайденные пользователи с именем 'Bob':")
for user in found_users:
    print(f"ID: {user.id}, Имя: {user.name}, Телефон: {user.phone}")


# Получение категорий по имени
found_categories = get_category_by_name("Electron")
print("\nНайденные категории с именем 'Electron':")
for category in found_categories:
    print(f"ID: {category.id}, Имя: {category.name}")


# Получение продуктов по имени
found_products = get_product_by_name("Smartphone")
print("\nНайденные продукты с именем 'Smartphone':")
for product in found_products:
    print(
        f"ID: {product.id}, Имя: {product.name}, Цена: {product.price}, Запас: {product.stock}, Категория ID: {product.category_id}"
    )
