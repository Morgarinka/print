import random
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from admin import admin_bp
from models import db
from models.product import Product


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)


@app.route("/", methods=["GET"])
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
