from database import Base
from sqlalchemy import Column, Integer, String,Boolean,Text,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    is_staff=Column(Boolean, default=False)
    is_active=Column(Boolean, default=True)
    orders = relationship('Choices', backref='user', lazy=True)
    

    def __repr__(self):
        return f"<User {self.username}>"
    
class Order(Base):
    ORDERS_STATUS=(
        ('Pending','pending'),
        ('In-Transit','In Progress'),
        ('Delivered','Delivered'),
    )

    PIZZA_SIZES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )

    __tablename__ =  'orders'
    id=Column(Integer, primary_key=True, index=True)
    quantity=Column(Integer, nullable=False)
    order_status=Column(ChoiceType(choices=ORDERS_STATUS), default='Pending')
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZES), default='Small')  
    user_id=Column(Integer, ForeignKey('users.id'))
    user=relationship('User', backref='orders')


    def __repr__(self):
        return f"<Order {self.id} - Status: {self.order_status}>"