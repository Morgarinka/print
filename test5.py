import random
import csv
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


# Добавляем товар
def add_product(name, description, price):
    session = Session()
    new_product = Product(name=name, description=description, price=price)
    session.add(new_product)
    session.commit
    session.close
#Функция добавление товара
def get_all_probucts():
    session=Session()
    products=session.query(Product).all()
    session.close()
    return products


# Генерация случайного товара
def generate_random_product():
    names = ["Хлеб", "Сахар", "Млоко", "Соль", "Конфеты", "Вода", "Яблоки"]
    desriptions = ["Белый", "Сладкий", "Свежее", "Круглые", "Минералтная", "Зеленые"]
    price = round(random.uniform(10, 100), 2)
    return random.choice(names), random.choice(desriptions), price


# Добавление 100 случайных товаров
for _ in range(100):
    product = generate_random_product()
    add_product(product[0], product[1], product[2])


# запись файла csv
def export_to_csv(filename):
    products = get_all_probucts()
    with open(filename, "w", newline="", encoding="utf=8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        csv_writer.writerow(["ID", "Название", "Описание", "Цена"])
        for product in products:
            csv_writer.writerow(
                [product.id, product.name, product.description, product.price]
            )


export_to_csv("products.csv")

def generate_html(filename):
    products = get_all_probucts()
    html_content = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Товары</title>
</head>
<body>
    <h1>Список товаров</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Описание</th>
            <th>Цена</th>
        </tr>
    '''
    for product in products:
        html_content += f'''
        <tr>
            <td>{product.id}</td>
            <td>{product.name}</td>
            <td>{product.description}</td>
            <td>{product.price}</td>
        </tr>
        '''

    html_content += '''
    </table>
</body>
</html>
'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

generate_html('products.html')

print("Товары успешно добавлены, экспортированы в CSV и HTML!")