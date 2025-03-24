from flask import render_template,request, redirect,url_for
from . import admin_bp
from models import db
from models.user import User

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
@admin_bp.route('/')
def abmin_indrx():
    return "admin_index"

@admin_bp.route("/users", methods=["GET", "POST"])
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