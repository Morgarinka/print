import random
import csv
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

engine = create_engine("sqlite:///products.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


Base.metadata.create_all(engine)
app = Flask(__name__)


# Добавляем товар
def add_product(name, description, price):
    session = Session()
    new_product = Product(name=name, description=description, price=price)
    session.add(new_product)
    session.commit()
    session.close()


# Функция получения товара
def get_all_probucts():
    session = Session()
    products = session.query(Product).all()
    session.close()
    return products


# Генерация случайного товара
def generate_random_products(num_products):
    for _ in range(num_products):
        name = f"Товар {random.randint(1, 1000)}"
        description = f"Описание {name}"
        price = round(random.uniform(1.0, 100.0), 2)
        add_product(name, description, price)

# запись файла csv
def export_to_csv():
    products = get_all_probucts()
    with open("products.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["id", "name", "description", "price"])
        for product in products:
            writer.writerow(
                [product.id, product.name, product.description, product.price]
            )


def generate_html():
    products = get_all_probucts()
    with open("products.html", "w", encoding="utf-8") as file:
        file.write(
            '<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><title>Товары</title></head><body>'
        )
        file.write(
            '<h1>Список товаров</h1><table border="1"><tr><th>ID</th><th>Название</th><th>Описание</th><th>Цена</th></tr>'
        )
        for product in products:
            file.write(
                f"<tr><td>{product.id}</td><td>{product.name}</td><td>{product.description}</td><td>{product.price}</td></tr>"
            )
        file.write("</table></body></html>")


@app.route("/")
def index():
    products = get_all_probucts()
    return render_template("products.html", products=products)


if __name__ == "__main__":
    generate_random_products(100)
    export_to_csv()
    generate_html()


app.run(debug=True)
