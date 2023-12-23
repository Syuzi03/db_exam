from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import relationship, declarative_base, Session, sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Product'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(50))
    manufacturer = Column(String(50))
    units_of_measurement = Column(Integer)

class Buyer(Base):
    __tablename__ = 'Buyer'
    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(100))
    phone = Column(String(20))
    contact_person = Column(String(50))

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


DATABASE_URL = "postgresql://postgres:pass123@localhost:5432/store"
engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

session.execute(text("CREATE USER syuzi WITH PASSWORD 'syuzi123'"))
session.execute(text("ALTER USER syuzi CREATEDB"))
session.execute(text("GRANT ALL PRIVILEGES ON DATABASE store TO syuzi"))

session.commit()
