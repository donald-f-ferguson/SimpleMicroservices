from pydantic import BaseModel, Field

class Consumer(BaseModel): 
    id: int = Field(
        ..., 
        description="Unique consumer identifier.", 
        example=1
    )
    first_name: str = Field(
        ..., 
        description="Consumer's first name.", 
        example="John"
    )
    last_name: str = Field(
        ..., 
        description="Consumer's last name.", 
        example="Doe"
    )
    email: str = Field(
        ..., 
        description="Consumer's email address.", 
        example="john.doe@example.com"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        }
    }