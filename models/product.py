from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(
        ...,
        description="Unique product identifier.",
        example=1001
    )
    name: str = Field(
        ...,
        description="Name of the product.",
        example="Laptop"
    )
    price: float = Field(
        ...,
        description="Price of the product.",
        example=999.99
    )
    description: str | None = Field(
        None,
        description="Detailed description of the product.",
        example="A high-performance laptop suitable for all your computing needs."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1001,
                "name": "Laptop",
                "price": 999.99,
                "description": "A high-performance laptop suitable for all your computing needs."
            }
        }
    }
