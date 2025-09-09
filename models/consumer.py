from pydantic import BaseModel, Field

class Consumer(BaseModel): 
    id: int
    first_name: str
    last_name: str
    email: str