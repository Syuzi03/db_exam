from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Session, sessionmaker

engine = create_engine("postgresql://syuzi:syuzi123@localhost:5432/store", echo=True)

Base = declarative_base()

def get_db():
    db = None
    try:
        db = sessionmaker(bind=engine)()
        yield db
    finally:
        if db is not None:
            db.close()

class Product(Base):
    __tablename__ = 'Product'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String)
    manufacturer = Column(String)
    units_of_measurement = Column(Integer)

class Buyer(Base):
    __tablename__ = 'Buyer'
    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    contact_person = Column(String)

class Purchase(Base):
    __tablename__ = 'Purchase'
    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)
    buyer_id = Column(Integer, ForeignKey('Buyer.buyer_id'), primary_key=True)
    delivery_date = Column(Date)
    unit_price = Column(Integer)
    quantity = Column(Integer)
    product = relationship('Product', back_populates='purchases')
    buyer = relationship('Buyer', back_populates='purchases')

Product.purchases = relationship('Purchase', order_by=Purchase.product_id, back_populates='product')
Buyer.purchases = relationship('Purchase', order_by=Purchase.buyer_id, back_populates='buyer')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
