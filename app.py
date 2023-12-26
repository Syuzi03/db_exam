from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from connection import Base, Product, Buyer, Purchase

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Use /docs to access the Swagger documentation."}

DATABASE_URL = "postgresql://syuzi:syuzi123@localhost:5432/store" 
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.get("/products/")
async def get_products(product_name: str = Query(None), manufacturer: str = Query(None)):
    query = session.query(Product)
    if product_name:
        query = query.filter(Product.product_name == product_name)
    if manufacturer:
        query = query.filter(Product.manufacturer == manufacturer)
    products = query.all()
    return [{'product_name': product.product_name, 'manufacturer': product.manufacturer} for product in products]

@app.get("/purchases/")
async def get_purchases(buyer_name: str = Query(None)):
    query = session.query(Purchase).join(Buyer).join(Product)
    if buyer_name:
        query = query.filter(Buyer.name == buyer_name)
    purchases = query.all()
    return [{'buyer_name': purchase.buyer.name, 'product_name': purchase.product.product_name} for purchase in purchases]

@app.put("/purchase/{purchase_id}")
async def update_purchase(purchase_id: int, unit_price: int):
    purchase = session.query(Purchase).filter_by(id=purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    purchase.unit_price = unit_price
    session.commit()
    return {'message': 'Purchase updated successfully'}

@app.get("/products/list/")
async def get_product_list(sort_by: str = Query(None)):
    query = session.query(Product)
    if sort_by:
        query = query.order_by(getattr(Product, sort_by))
    products = query.all()
    return [{'product_name': product.product_name, 'manufacturer': product.manufacturer} for product in products]

@app.get("/purchases/")
async def get_purchases(
    buyer_name: str = Query(None),
    sort_by: str = Query(None)
):
    query = session.query(Purchase).join(Buyer).join(Product)
    
    if buyer_name:
        query = query.filter(Buyer.name == buyer_name)
    
    # Сортировка результатов по заданному полю
    if sort_by:
        # Поддерживаем сортировку по полям Product и Buyer
        sort_column = getattr(Purchase.product, sort_by, None) or getattr(Buyer, sort_by, None)
        if sort_column:
            query = query.order_by(sort_column)

    purchases = query.all()
    
    return [{'buyer_name': purchase.buyer.name, 'product_name': purchase.product.product_name} for purchase in purchases]
