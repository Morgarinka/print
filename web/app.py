import random
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from admin import admin_bp
from models import db
from models import Product,Category
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"


#db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category_id = request.form.get("category_id")

        new_product = Product(name=name, description=description, price=price, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("index"))

    categories = Category.query.all()  # Получаем все категории для выпадающего списка
    return render_template("add_product.html", categories=categories)




@app.route("/", methods=["GET"])
def index():
    # Получаем все продукты
    products = Product.query.all()
    random_products = random.sample(products, min(len(products), 10))
    return render_template("index.html", products=random_products)


# Страница добавление товара
@app.route("/admin/product", methods=["GET", "POST"])
def admin_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")

        if name and price:
            new_product = Product(
                name=name, description=description, price=float(price)
            )
            db.session.add(new_product)
            db.session.commit()
        return redirect(url_for("index"))

    return render_template("admin_product.html")


# Страница управления пользователями
@app.route("/admin/users", methods=["GET", "POST"])
def admin_users():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("admin_users"))

    users = User.query.all()
    
    return render_template("admin_users.html", users=users)



app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
