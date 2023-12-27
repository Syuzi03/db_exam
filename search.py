from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from connection import Product, Buyer

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Use /docs to access the Swagger documentation."}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://syuzi:syuzi123@localhost:5432/store"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/fulltextsearch/{table_name}")
async def full_text_search(table_name: str, query: str, db: Session = Depends(get_db)):
    if table_name == 'Product':
        model = Product
        column = Product.product_name
    elif table_name == 'Buyer':
        model = Buyer
        column = Buyer.name
    else:
        raise HTTPException(status_code=404, detail="Table not found")

    results = db.query(model).filter(column.ilike(f"%{query}%")).all()

    return {"results": results}
