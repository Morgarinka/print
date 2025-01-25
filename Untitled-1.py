from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    REAL,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session, relationship

Base = declarative_base()
engine = create_engine("sqlite:///test2.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


class Order(Base):
    __tablename__ = "ordes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_id", nullabe=False))
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    items = relationship("Orderitem", back_populates="order")


class Orderitem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products_id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(REAL, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


User.orders = relationship("Order", order_by=Order.id, back_populates="user")

Base.metadata.create_all(engine)


def create_order(user_id: int, order_items: list):
    with SessionLocal() as session:
        # Проверка наличия пользователя
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"Ошибка: Пользователь с ID {user_id} не найден.")
            return None

        # создание нового класса
        new_order = Order(user_id=user_id)
        session.add(new_order)
        session.commit()

        total_price = 0

        for item in order_items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            # Проверка на наличия продукта
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                print(f"Ошибка: Продукт с ID {product_id} не найден.")
                continue
            # ПРоверка на наличие на складе
            if quantity > product.stock:
                print(f"Ошибка: Недостаточно на складе для продукта {product.name}.")
                continue

            total_price += product.price * quantity
            # Создание заказа
            order_item = Orderitem(
                order_id=new_order.id,
                product_id=product_id,
                quantity=quantity,
                price=product.price,
            )
            session.add(order_item)

            # обновление заказа
            product.stock -= quantity
            # Сохраняем элементы заказа
            session.commit()
            print(
                f"Заказ с ID {new_order.id} успешно оформлен. Итоговая сумма: {total_price:.2f}"
            )
        return new_order


def get_order_status(order_id: int):
    with SessionLocal() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            print(f"Ошибка: Заказ с ID {order_id} не найден.")
            return None
        return order.status


def update_order_status(order_id: int, new_status: str):
    valid_statuses = ["pending", "completed", "canceled"]
    if new_status not in valid_statuses:
        print(
            f"Ошибка: Неверный статус '{new_status}'. Допустимые статусы: {valid_statuses}."
        )
        return False

    with SessionLocal() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            print(f"Ошибка: Заказ с ID {order_id} не найден.")
            return False

        order.status = new_status
        session.commit()
        print(f"Статус заказа с ID {order_id} обновлен на '{new_status}'.")
        return True


def add_user(name: str, phone: str):
    with SessionLocal() as session:
        if session.query(User).filter_by(phone=phone).first():
            print(f"Ошибка: Пользователь с телефоном {phone} уже существует.")
            return
        new_user = User(name=name, phone=phone)
        session.add(new_user)
        session.commit()
        print(f"Добавлен пользователь: {name}, телефон: {phone}")


def add_categoty(name: str):
    with SessionLocal() as session:
        if session.query(Category).filter_by(name=name).first():
            print(f"Ошибка: Категория {name} уже существует.")
            return
        new_category = Category(name=name)
        session.add(new_category)
        session.commit()
        print(f"Добавлена категория: {name}")


def add_product(
    name: str, description: str, price: float, stock: int, category_id: int
):
    with SessionLocal() as session:
        if session.query(Product).filter_by(name=name, category_id=category_id).first():
            print(f"Ошибка: Продукт {name} в категории {category_id} уже существует.")
            return
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


if __name__ == "main":
    add_user("Bob", "+723-456-7890")
    add_user("Alex", "+855-465-5457")
    add_category("Electron")
    add_category("Textile")
    add_product("Smartphone", "new model", 699.99, 50, 1)
    add_product("Knitwear", "white", 123, 22, 2)

    # Оформление заказа
    create_order(
        1, [{"product_id": 1, "quantity": 2}, {"product_id": 2, "quantity": 1}]
    )

    # Получение всех пользователей
    users = get_all_users()
    print("Все пользователи:")
    for user in users:
        print(f"ID: {user.id}, Имя: {user.name}, Телефон: {user.phone}")

    # Получение всех категорий
    categories = get_order_status()
    print("\nВсе категории:")
    for category in categories:
        print(f"ID: {category.id}, Имя: {category.name}")

    # Получение всех продуктов
    products = get_order_status()
    print("\nВсе продукты:")
    for product in products:
        print(
            f"ID: {product.id}, Имя: {product.name}, Цена: {product.price}, Запас: {product.stock}, Категория ID: {product.category_id}"
        )

    # Получение статуса заказа
    get_order_status(1)
    print(f"\nСтатус заказа 1: {order_status}")

    # Изменение статуса заказа
    update_order_status(1, "completed")
