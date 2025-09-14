from __future__ import annotations

import os
import socket
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, Path

# Existing imports
from models.health import Health
from models.consumer import Consumer

# New imports
from pydantic import BaseModel, Field

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
products: Dict[UUID, "ProductRead"] = {}
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
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Unit price of the product")


class ProductRead(ProductCreate):
    id: UUID


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


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
# Consumer Endpoints
# -----------------------------------------------------------------------------
@app.get("/consumers", response_model=List[Consumer])
def list_consumers():
    return list(consumers.values())


@app.get("/consumers/{consumer_id}", response_model=Consumer)
def get_consumer(consumer_id: int = Path(..., description="ID of the consumer")):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    return consumers[consumer_id]


@app.post("/consumers", response_model=Consumer)
def create_consumer(consumer: Consumer):
    if consumer.id in consumers:
        raise HTTPException(status_code=400, detail="Consumer already exists")
    consumers[consumer.id] = consumer
    return consumer


@app.put("/consumers/{consumer_id}", response_model=Consumer)
def put_consumer(consumer_id: int, consumer: Consumer):
    consumer.id = consumer_id
    consumers[consumer_id] = consumer
    return consumer


@app.patch("/consumers/{consumer_id}", response_model=Consumer)
def patch_consumer(consumer_id: int, update: Consumer):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    stored = consumers[consumer_id].dict()
    stored.update(update.dict(exclude_unset=True))
    consumers[consumer_id] = Consumer(**stored)
    return consumers[consumer_id]


@app.delete("/consumers/{consumer_id}", response_model=dict)
def delete_consumer(consumer_id: int):
    if consumer_id not in consumers:
        raise HTTPException(status_code=404, detail="Consumer not found")
    del consumers[consumer_id]
    return {"detail": f"Consumer {consumer_id} deleted"}


# -----------------------------------------------------------------------------
# Product Endpoints
# -----------------------------------------------------------------------------
@app.get("/products", response_model=List[ProductRead])
def list_products():
    return list(products.values())


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]


@app.post("/products", response_model=ProductRead)
def create_product(product: ProductCreate):
    product_id = uuid4()
    new_product = ProductRead(id=product_id, **product.dict())
    products[product_id] = new_product
    return new_product


@app.put("/products/{product_id}", response_model=ProductRead)
def put_product(product_id: UUID, product: ProductCreate):
    new_product = ProductRead(id=product_id, **product.dict())
    products[product_id] = new_product
    return new_product


@app.patch("/products/{product_id}", response_model=ProductRead)
def patch_product(product_id: UUID, update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    stored = products[product_id].dict()
    stored.update(update.dict(exclude_unset=True))
    products[product_id] = ProductRead(**stored)
    return products[product_id]


@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: UUID):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return {"detail": f"Product {product_id} deleted"}


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