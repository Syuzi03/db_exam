from datetime import date
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "postgresql://syuz:syuz123@localhost/store"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    purchases = relationship('Purchase', back_populates='buyer')

class Purchase(Base):
    __tablename__ = 'Purchase'
    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)
    buyer_id = Column(Integer, ForeignKey('Buyer.buyer_id'), primary_key=True)
    delivery_date = Column(Date)
    unit_price = Column(Integer)
    quantity = Column(Integer)
    product = relationship('Product', back_populates='purchases')
    buyer = relationship('Buyer', back_populates='purchases')

Base.metadata.create_all(bind=engine)

class ProductCreate(BaseModel):
    product_name: str
    manufacturer: str
    units_of_measurement: int

class ProductUpdate(BaseModel):
    product_name: str = None
    manufacturer: str = None
    units_of_measurement: int = None

class BuyerCreate(BaseModel):
    name: str
    address: str
    phone: str
    contact_person: str

class BuyerUpdate(BaseModel):
    name: str = None
    address: str = None
    phone: str = None
    contact_person: str = None

class PurchaseCreate(BaseModel):
    product_id: int
    buyer_id: int
    delivery_date: date
    unit_price: int
    quantity: int

class PurchaseUpdate(BaseModel):
    delivery_date: date = None
    unit_price: int = None
    quantity: int = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        for key, value in updated_product.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    
@app.post("/buyers/")
def create_buyer(buyer: BuyerCreate, db: Session = Depends(get_db)):
    db_buyer = Buyer(**buyer.dict())
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer

@app.get("/buyers/{buyer_id}")
def read_buyer(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.buyer_id == buyer_id).first()
    if buyer:
        return buyer
    else:
        raise HTTPException(status_code=404, detail="Buyer not found")

@app.put("/buyers/{buyer_id}")
def update_buyer(buyer_id: int, updated_buyer: BuyerUpdate, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.buyer_id == buyer_id).first()
    if buyer:
        for key, value in updated_buyer.dict(exclude_unset=True).items():
            setattr(buyer, key, value)
        db.commit()
        db.refresh(buyer)
        return buyer
    else:
        raise HTTPException(status_code=404, detail="Buyer not found")

@app.delete("/buyers/{buyer_id}")
def delete_buyer(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.buyer_id == buyer_id).first()
    if buyer:
        db.delete(buyer)
        db.commit()
        return {"message": "Buyer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Buyer not found")

@app.post("/purchases/")
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/{product_id}/{buyer_id}")
def read_purchase(product_id: int, buyer_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.product_id == product_id, Purchase.buyer_id == buyer_id).first()
    if purchase:
        return purchase
    else:
        raise HTTPException(status_code=404, detail="Purchase not found")

@app.put("/purchases/{product_id}/{buyer_id}")
def update_purchase(product_id: int, buyer_id: int, updated_purchase: PurchaseUpdate, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.product_id == product_id, Purchase.buyer_id == buyer_id).first()
    if purchase:
        for key, value in updated_purchase.dict(exclude_unset=True).items():
            setattr(purchase, key, value)
        db.commit()
        db.refresh(purchase)
        return purchase
    else:
        raise HTTPException(status_code=404, detail="Purchase not found")

@app.delete("/purchases/{product_id}/{buyer_id}")
def delete_purchase(product_id: int, buyer_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchase).filter(Purchase.product_id == product_id, Purchase.buyer_id == buyer_id).first()
    if purchase:
        db.delete(purchase)
        db.commit()
        return {"message": "Purchase deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Purchase not found")