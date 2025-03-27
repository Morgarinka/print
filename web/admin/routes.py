from flask import render_template, request, redirect, url_for
from . import admin_bp
from models import db
from models.user import User
from models.product import Product
import random


@admin_bp.route("/")
def abmin_indrx():
    all_products = Product.query.all()

    random_products = random.sample(all_products, min(len(all_products), 10))
    return render_template(
        "index.html", products=random_products, all_products=all_products
    )


# Страница управления пользователями
@admin_bp.route("/users", methods=["GET", "POST"])
def admin_users():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("admin/users"))

    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/product", methods=["GET", "POST"])
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
        return redirect(url_for("admin/product"))
    product = Product.query.all()

    return render_template("admin/product.html")
