from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# Pydantic v2: small model_config to enable from_attributes if needed later
class EmployeeBase(BaseModel):
    name: str
    email: str
    position: str

    model_config = {"extra": "forbid"}


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None

    model_config = {"extra": "forbid"}


class EmployeeRead(EmployeeBase):
    id: UUID

    model_config = {"json_schema_extra": {"example": {"id": "uuid", "name": "Alice"}}}
