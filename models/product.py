from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float