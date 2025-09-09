from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query, Path

# Existing imports
from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.consumer import Consumer

# New imports
from pydantic import BaseModel, Field

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------

persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
products: Dict[UUID, "ProductRead"] = {}
orders: Dict[UUID, "OrderRead"] = {}
# In-memory database for consumers (using int as key, matching Consumer.id type)
consumers: Dict[int, Consumer] = {}

app = FastAPI(
    title="Person/Address/Product/Order API",
    description="Demo FastAPI app using Pydantic v2 models",
    version="0.2.0",
)

# -----------------------------------------------------------------------------
# New Models (with type annotations)
# -----------------------------------------------------------------------------
class ProductCreate(BaseModel):
    id: int = Field(..., description="Unique identifier for the product")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Unit price of the product")


class ProductRead(ProductCreate):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class OrderCreate(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int = Field(..., gt=0, description="Number of items ordered")


class OrderRead(OrderCreate):
    total_price: float


class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)


# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo,
    )


@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)


@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------
@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]


@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    postal_code: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
):
    results = list(addresses.values())
    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]
    return results


@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]


@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]


# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read


@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    birth_date: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
):
    results = list(persons.values())
    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]
    return results


@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]


@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]


# -----------------------------------------------------------------------------
# Product endpoints
# -----------------------------------------------------------------------------
@app.post("/products", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate):
    if product.id in products:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products[product.id] = ProductRead(**product.model_dump())
    return products[product.id]


@app.get("/products", response_model=List[ProductRead])
def list_products():
    return list(products.values())


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]


@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    stored = products[product_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    products[product_id] = ProductRead(**stored)
    return products[product_id]


# -----------------------------------------------------------------------------
# Order endpoints
# -----------------------------------------------------------------------------
@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate):
    if order.id in orders:
        raise HTTPException(status_code=400, detail="Order with this ID already exists")
    if order.product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found for this order")
    product = products[order.product_id]
    total_price = order.quantity * product.price
    order_read = OrderRead(**order.model_dump(), total_price=total_price)
    orders[order.id] = order_read
    return order_read


@app.get("/orders", response_model=List[OrderRead])
def list_orders():
    return list(orders.values())


@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: UUID):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]


@app.patch("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: UUID, update: OrderUpdate):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    stored = orders[order_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    if "quantity" in stored and stored["quantity"] and stored["product_id"] in products:
        product = products[stored["product_id"]]
        stored["total_price"] = stored["quantity"] * product.price
    orders[order_id] = OrderRead(**stored)
    return orders[order_id]

@app.post("/consumers", response_model=Consumer, status_code=201)
def create_consumer(consumer: Consumer):
    if consumer.id in consumers:
        raise HTTPException(status_code=400, detail="Consumer ID already exists")
    consumers[consumer.id] = consumer
    return consumer

# ----------------------
# List Consumers
# ----------------------
@app.get("/consumers", response_model=List[Consumer])
def list_consumers():
    return list(consumers.values())

# ----------------------
# Get Consumer by ID
# ----------------------
@app.get("/consumers/{consumer_id}", response_model=Consumer)
def get_consumer(consumer_id: int = Path(..., description="ID of the consumer")):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return consumers[consumer_id]

# ----------------------
# Update Consumer
# ----------------------
@app.patch("/consumers/{consumer_id}", response_model=Consumer)
def update_consumer(consumer_id: int, update: Consumer):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    stored = consumers[consumer_id].dict()
    stored.update(update.dict(exclude_unset=True))
    consumers[consumer_id] = Consumer(**stored)
    return consumers[consumer_id]

# ----------------------
# Delete Consumer
# ----------------------
@app.delete("/consumers/{consumer_id}", response_model=dict)
def delete_consumer(consumer_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    del consumers[consumer_id]
    return {"detail": f"Consumer {consumer_id} deleted"}

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/Product/Order API. See /docs for OpenAPI UI."}


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
