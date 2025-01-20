from sqlalchemy import create_engine, Column, Integer, String, Text, REAL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session, relationship

Base = declarative_base()

engine = create_engine("sqlite:///test.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(REAL, nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


Category.products = relationship(
    "Product", order_by=Product.id, back_populates="category"
)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def add_user(name: str, phone: str):
    with SessionLocal() as session:
        new_user = User(name=name, phone=phone)
        session.add(new_user)
        session.commit()

    print(f"Добавлен пользователь: {name},телефон:{phone}")


def add_category(name: str):
    with SessionLocal() as session:
        new_category = Category(name=name)
        session.add(new_category)
        session.commit()

    print(f"Добавлена категоря:{name}")


def add_product(name: str, description: str, price: float, stock: int, category_id: int):
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
#Фильтр по всем категориям
def get_all_users():
    with SessionLocal()as session:
        users=session.query(User).all()
        return users

def get_all_categories():
    with SessionLocal()as session:
        categories=session.query(Category).all()
        return categories

def get_all_products():
    with SessionLocal()as session:
        products=session.query(Product).all()
        return products
#Фильтр по имени
def get_user_by_name(name:str):
    with SessionLocal()as session:
        user=session.query(User).filter(User.name==name).all()
        return user
    
def get_category_by_name(name:str):
    with SessionLocal()as session:
        category=session.query(Category).filter(Category.name==name).all()
        return category

def get_product_by_name(name:str):
    with SessionLocal()as session:
        product=session.query(Product).filter(Product.name==name).all()
        return product


if __name__ == "__main__":
    add_user('Bob', '+723-456-7890')
    add_category('Electron')
    add_product('Smartphone', 'new model', 699.99, 50, 1)