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
                        OrderItem)
from .api_models import (ProductPublic, ProductCreate, 
                         CountryCreate, CountryPublic, 
                         CustomerPublic, CustomerCreate, 
                         StatusPublic, StatusCreate,
                         OrderCreate, OrderPublic, OrderUpdate,
                         OrderItemPublic)

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

@app.get("/health/")
def healthcheck(session: SessionDep):
    return {"health": "ok"}

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
    # get customer making the order
    get_customer_statement = select(Customer).where(Customer.id == order.customer_id)
    customer_results = session.exec(get_customer_statement)
    customer = customer_results.first()

    # if customer doesn't exist throw an error
    if not customer:
        raise HTTPException(status_code=404, detail="Customer was not found")

    # get status Pending for creating the order
    get_status_statement = select(Status).where(Status.name == "Pending")
    status_results = session.exec(get_status_statement)
    status = status_results.first()

    # if status for Pending doesn't exist throw an error
    if not status:
        raise HTTPException(status_code=404, detail="Pending order status was not found")

    try:
        # the order data to be inserted to orders table
        order_data = Order(
            current_status_id = status.id,
            customer_id = order.customer_id,
            tax_amount = order.tax_amount,
            discount_amount = order.discount_amount,
            shipping_costs_amount = order.shipping_costs_amount
        )

        # add the new order data
        session.add(order_data)
        session.flush()
        session.refresh(order_data)

        print(f"ORDER DATA: {order_data}")    

        # items array to show in output
        items_arr = []

        # loop through items for the order
        for item in order.items:
            # get the product from the products table
            product = session.get(Product, item.product_id)
            
            # if not found, throw an error
            if not product:
                raise HTTPException(status_code=404, detail="Product was not found")
        
            # the item to add to the order_items table
            item_to_add = OrderItem(
                product_id = product.id,
                order_id = order_data.id,
                quantity = item.quantity,
                price_per_unit_at_purchase = product.current_price_online
            )

            # add the item to the order_items table
            session.add(item_to_add)
            session.flush()
            session.refresh(item_to_add)
            print(f"ITEM TO ADD: {item_to_add}")

            # get the item data
            item_data = OrderItemPublic(
               **item_to_add.model_dump(),
               product_name = product.name
            )

            # push to array for output
            items_arr.append(item_data)

        #print(f"ITEMS ARRAY FOR OUTPUT: {items_arr}")

        # build output
        output = OrderPublic(
            **order_data.model_dump(),
            customer_name = customer.name,
            current_status_name = status.name,
            order_items = items_arr
        )

        session.commit()
        return output
    except:
        session.rollback()
        raise

# endpoint to update status of an order
@app.patch("/orders/{order_id}", response_model=OrderPublic)
def update_order(order_id: int, order: OrderUpdate, session: SessionDep):
    print(f"order: {order}")

    # get the order from the orders table
    order_db = session.get(Order, order_id)

    # if order was not found throw error
    if not order_db:
        raise HTTPException(status_code=404, detail="Order was not found")

    # get the new status from the status table
    get_status_statement = select(Status).where(Status.id == order.current_status_id)
    status_results = session.exec(get_status_statement)
    status = status_results.first()

    # if status doesn't exist throw an error
    if not status:
        raise HTTPException(status_code=404, detail="Status was not found")

    # get customer making the order
    get_customer_statement = select(Customer).where(Customer.id == order_db.customer_id)
    customer_results = session.exec(get_customer_statement)
    customer = customer_results.first()

    # if customer doesn't exist thrown an error
    if not customer:
        raise HTTPException(status_code=404, detail="Customer was not found")

    # get order items for the order
    get_order_items_statement = select(OrderItem).where(OrderItem.order_id == order_db.id)
    order_items_results = session.exec(get_order_items_statement)
    order_items = order_items_results.all()

    # if no order items found, throw error
    if not order_items:
        raise HTTPException(status_code=404, detail="Order items were not found")

    # items array for output
    items_arr = []

    for ord_item in order_items:
        # get the product from the products table
        product = session.get(Product, ord_item.product_id)
            
        # if not found, throw an error
        if not product:
            raise HTTPException(status_code=404, detail="Product was not found")

        item_data = OrderItemPublic(
            id = ord_item.id,
            product_id = ord_item.product_id,
            order_id = ord_item.order_id,
            quantity = ord_item.quantity,
            price_per_unit_at_purchase = ord_item.price_per_unit_at_purchase,
            product_name = product.name
        )

        items_arr.append(item_data)

    # preview the items_array for output
    #print(f"ITEMS ARRAY FOR OUTPUT: {items_arr}")

    # get the data to update the order with
    order_update_data = order.model_dump(exclude_unset=True)

    # update the existing order with the new data
    order_db.sqlmodel_update(order_update_data)

    # commit the changes
    session.add(order_db)
    session.commit()
    session.refresh(order_db)

    return OrderPublic(
        **order_db.model_dump(),
        customer_name = customer.name,
        current_status_name = status.name,
        order_items = items_arr
    )

# get products
@app.get("/products/", response_model=list[ProductPublic])
def read_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Product]:
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products

# get statuses
@app.get("/status/", response_model=list[StatusPublic])
def read_status(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
) -> list[Status]:
    status = session.exec(select(Status).offset(offset).limit(limit)).all()
    return status

# get customers
@app.get("/customers/", response_model=list[CustomerPublic])
def read_customers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Customer]:
    customers = session.exec(select(Customer.id, 
                                    Customer.username, 
                                    Customer.email,
                                    Customer.name,
                                    Customer.country_id, 
                                    Country.name.label("country_name"))
                            .join(Country).offset(offset).limit(limit)).all()
    return customers

# get orders
@app.get("/orders/", response_model=list[OrderPublic])
def read_orders(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Order]:
    orders = session.exec(select(Order).offset(offset).limit(limit)).all()

    output_arr = []
    for order in orders:
        # get customer making the order
        get_customer_statement = select(Customer).where(Customer.id == order.customer_id)
        customer_results = session.exec(get_customer_statement)
        customer = customer_results.first()

        # if customer wasn't found throw error
        if not customer:
            raise HTTPException(status_code=404, detail="Customer was not found")

        # get order's status from the status table
        get_status_statement = select(Status).where(Status.id == order.current_status_id)
        status_results = session.exec(get_status_statement)
        status = status_results.first()

        # if status wasn't found throw error
        if not status:
            raise HTTPException(status_code=404, detail="Status was not found")

        # get order items for the order
        get_order_items_statement = select(OrderItem).where(OrderItem.order_id == order.id)
        order_items_results = session.exec(get_order_items_statement)
        order_items = order_items_results.all()

        # if no order items found, throw error
        if not order_items:
            raise HTTPException(status_code=404, detail="Order items were not found")

        # items array for output
        items_arr = []

        # handle order items 
        for ord_item in order_items:
            # get the product from the products table
            product = session.get(Product, ord_item.product_id)
                
            # if not found, throw an error
            if not product:
                raise HTTPException(status_code=404, detail="Product was not found")

            item_data = OrderItemPublic(
                id = ord_item.id,
                product_id = ord_item.product_id,
                order_id = ord_item.order_id,
                quantity = ord_item.quantity,
                price_per_unit_at_purchase = ord_item.price_per_unit_at_purchase,
                product_name = product.name
            )

            items_arr.append(item_data)

        # preview the items_array for output
        #print(f"ITEMS ARRAY FOR OUTPUT: {items_arr}")

        output_arr.append(
            OrderPublic(
                **order.model_dump(),
                customer_name = customer.name,
                current_status_name = status.name,
                order_items = items_arr
            )
        )

    return output_arr

# get uncompleted orders (current_status is not 'Completed')
@app.get("/uncompleted_orders/", response_model=list[OrderPublic])
def read_orders(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Order]:
    orders = session.exec(select(Order).join(Status).offset(offset).limit(limit).where(Status.name != "Completed")).all()
    
    output_arr = []
    for order in orders:
        # get customer making the order
        get_customer_statement = select(Customer).where(Customer.id == order.customer_id)
        customer_results = session.exec(get_customer_statement)
        customer = customer_results.first()
        
        # if customer wasn't found throw error
        if not customer:
            raise HTTPException(status_code=404, detail="Customer was not found")

        # get order's status from the status table
        get_status_statement = select(Status).where(Status.id == order.current_status_id)
        status_results = session.exec(get_status_statement)
        status = status_results.first()

        # if status wasn't found throw error
        if not status:
            raise HTTPException(status_code=404, detail="Status was not found")

        # get order items for the order
        get_order_items_statement = select(OrderItem).where(OrderItem.order_id == order.id)
        order_items_results = session.exec(get_order_items_statement)
        order_items = order_items_results.all()

        # if no order items found, throw error
        if not order_items:
            raise HTTPException(status_code=404, detail="Order items were not found")

        # items array for output
        items_arr = []

        # handle order items 
        for ord_item in order_items:
            # get the product from the products table
            product = session.get(Product, ord_item.product_id)
                
            # if not found, throw an error
            if not product:
                raise HTTPException(status_code=404, detail="Product was not found")

            item_data = OrderItemPublic(
                id = ord_item.id,
                product_id = ord_item.product_id,
                order_id = ord_item.order_id,
                quantity = ord_item.quantity,
                price_per_unit_at_purchase = ord_item.price_per_unit_at_purchase,
                product_name = product.name
            )

            items_arr.append(item_data)

        # preview the items_array for output
        #print(f"ITEMS ARRAY FOR OUTPUT: {items_arr}")
        
        output_arr.append(
            OrderPublic(
                **order.model_dump(),
                customer_name = customer.name,
                current_status_name = status.name,
                order_items = items_arr
            )
        )

    return output_arr