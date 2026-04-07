from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from .database import setup_db, get_engine
from .db_models import (Product, 
                        Country, 
                        Customer, 
                        Status, 
                        Order,
                        OrderItem,
                        StatusHistory)
from .api_models import (ProductPublic, ProductCreate, 
                         CountryCreate, CountryPublic, 
                         CustomerPublic, CustomerCreate, 
                         StatusPublic, StatusCreate,
                         OrderCreate, OrderPublic,
                         OrderItemCreate, OrderItemPublic)

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

# endpoint to create a product
@app.post("/products/", response_model=ProductPublic)
def create_product(product: ProductCreate, session: SessionDep):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

# endpoint to create a country
@app.post("/countries/", response_model=CountryPublic)
def create_country(country: CountryCreate, session: SessionDep):
    db_country = Country.model_validate(country)
    session.add(db_country)
    session.commit()
    session.refresh(db_country)
    return db_country

# endpoint to create customer
@app.post("/customers/", response_model=CustomerPublic)
def create_customer(customer: CustomerCreate, session: SessionDep):
    db_customer = Customer.model_validate(customer)

    # get country based on the country_id input
    country = session.get(Country, db_customer.country_id)

    # if no country was found, show error
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    else:
        # get the country's name
        country_name = country.name

        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)

        # return the customers table fields + the country's name
        return CustomerPublic(
            id=db_customer.id,
            name=db_customer.name,
            email=db_customer.email,
            username=db_customer.username,
            country_name=country_name,
            country_id=db_customer.country_id
        )

# endpoint to create a status
@app.post("/status/", response_model=StatusPublic)
def create_status(status: StatusCreate, session: SessionDep):
    db_status = Status.model_validate(status)
    session.add(db_status)
    session.commit()
    session.refresh(db_status)
    return db_status

# endpoint to create an order
@app.post("/orders/", response_model=OrderPublic)
def create_order(order: OrderCreate, session: SessionDep):
    get_status_statement = select(Status).where(Status.name == "Pending")
    status_results = session.exec(get_status_statement)
    status = status_results.first()

    if not status:
        raise HTTPException(status_code=404, detail="Pending order status not found")
    else:
        try:
            order_data = Order(
                current_status_id = status.id,
                customer_id = order.customer_id,
                total_amount = order.total_amount
            )

            session.add(order_data)
            session.flush()
            session.refresh(order_data)

            print(f"ORDER DATA: {order_data}")    

            for item in order.items:
                product = session.get(Product, item.product_id)
                
                if not product:
                    raise HTTPException(status_code=404, detail="Country not found")
                else:
                    item_to_add = OrderItem(
                        product_id = product.id,
                        order_id = order_data.id,
                        quantity = item.quantity,
                        price_at_purchase = product.current_price
                    )
                    session.add(item_to_add)
                    session.flush()
                    session.refresh(item_to_add)
                    print(f"ITEM TO ADD: {item_to_add}")

            status_history_to_add = StatusHistory( 
                order_id = order_data.id,
                status_id = status.id
            )

            session.add(status_history_to_add)
            session.flush()
            session.refresh(status_history_to_add)
            print(f"STATUS HISTORY TO ADD:{status_history_to_add}")

            session.commit()

            return order_data
        except:
            session.rollback()
            raise