from sqlalchemy import Column, Integer, String
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    order_item = Column(String)
    address = Column(String)
    postal_code = Column(String)
    status = Column(String)