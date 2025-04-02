from flask import render_template, request, redirect, url_for
from . import admin_bp
from models import db
from models.user import User
from models.product import Product
import random
from models.category import Category
from models.Order import Order
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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

#Маршрут для отображения продуктов категории
@admin_bp.route('/category/<int:category_id>',methost=['GET'])
def category_products(categoty_id):
    products=Product.query.filter_by(categoty_id).all()

    random_products=random.sample(products,min(len(products),10))
    category=Category.query.get(categoty_id)
    return render_template('category_products.html',products=random_products,category=category)

@admin_bp.route('/create_order/<int:user_id>',methods=['POST'])
def create_order(user_id):
    status='Корзина'
    new_order=Order(user_id=user_id,status=status)

    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('index'))

@admin_bp.route("/add_product", methods=["GET", "POST"])
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

@admin_bp.route('/category/<int:category_id>',methods=['GRT'])
def get_category(category_id):
    category=Category.query.get(category_id)
    if category:
        return render_template('category.html',category=category)
    else:
        
        return "Категория не найдена"

@admin_bp.route('/categories',methods=['GET'])
def show_categories():
    categoryes= Category.query.all()
    return render_template('categories.html',categoryes=categoryes)

@admin_bp.route("/register",methods=['GET',"POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        if username and password:
            hashed_password=generate_password_hash(password)
            new_user=User(username=username,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("Login"))
        return render_template("register.html")
    

@admin_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=User.query.filter_by(username=username).first

        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("index"))
        return render_template("logon.html")


