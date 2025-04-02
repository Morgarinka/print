import random
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from admin import admin_bp
from models import db
from models.product import Product
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)
app.secret_key="qwer"

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="Login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)



app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
