from sqlalchemy import create_engine, Column, Integer, String, Text, REAL, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session, relationship


class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,nullable=False)
    name=Column(Text,nullable=False)
    phone=Column(Text,nullable=False)
    orders=relationship('Order',back_populates='user')

def create_user(user_id:int,name:str,phone:str):
    with SessionLocal() as session:
        existing_user=session.query(User).filter(user.user_id==user_id).first()
        if existing_user:
            print(f"Пользователь с ID {user_id} уже существует.")
            return None
        new_user=User(user_id=user_id,name=name,phone=phone)
        session.add(new_user)
        session.commit()
        print(f"Добавлен пользователь: {name}, телефон: {phone}")
        return new_user
def get_user(user_id:int):
    with SessionLocal()as session:
        return session.query(User).filter(User.id==user_id).first()
    