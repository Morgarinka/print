import random
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from admin import admin_bp
from models import db
from models.product import Product
from models.category import Category


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)


@app.route("/", methods=["GET"])
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


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

    categories = Category.query.all()  
    return render_template("add_product.html", categories=categories)


@app.route('/category/<int:category_id>',methost=['GET'])
def category_products(categoty_id):
    products=Product.query.filter_by(categoty_id).all()

    random_products=random.sample(products,min(len(products),10))
    category=Category.query.get(categoty_id)
    return render_template('category_products.html',products=random_products,category=category)

app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
