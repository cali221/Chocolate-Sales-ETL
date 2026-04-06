from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import Session
from .db_models import Product, Country, Customer, Status, Order, StatusHistory, OrderProduct
from .database import setup_db, get_engine

engine = get_engine()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('LIFESPAN START')
    setup_db(engine)
    yield
    print('LIFESPAN END')
    
app = FastAPI(lifespan=lifespan)

@app.post("/products/")
def create_product(product: Product, session: SessionDep) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product