from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID


class PaycheckBase(BaseModel):
    employee_id: UUID
    amount: float
    date_issued: date

    model_config = {"extra": "forbid"}


class PaycheckCreate(PaycheckBase):
    pass


class PaycheckUpdate(BaseModel):
    employee_id: Optional[UUID] = None
    amount: Optional[float] = None
    date_issued: Optional[date] = None

    model_config = {"extra": "forbid"}


class PaycheckRead(PaycheckBase):
    id: UUID
