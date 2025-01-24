from sqlalchemy import create_engine, Column, Integer, String, Text, REAL, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session, relationship

Base= declarative_base()

class Order(Base):
    __tablename__='ordes'
    
    id= Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('user_id',nullabe=False))
    status=Column(String,default='pending')

    user=relationship('User',back_populates='orders')
    items=relationship('Orderitem',back_populates='order')


class Orderitem(Base):
    __tablename__='order_items'

    id=Column(Integer,primary_key=True)
    order_id=Column(Integer,ForeignKey('orders_id'),nullable=False)
    product_id=Column(Integer,ForeignKey('products_id'),nullable=False)
    quantity=Column(Integer,default=1)
    price=Column(REAL,nullable=False)

    order=relationship('Order',back_populates='items')
    product=relationship('Product')

User.orders=relationship('Order',order_by=Order.id,back_populates='user')