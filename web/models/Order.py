from flask_sqlalchemy import SQLAlchemy
from models.user import User
db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('Корзина', 'Оформлен', 'Оплачен', 'Исполнен'), nullable=False)

    user = db.relationship('User', backref='orders')