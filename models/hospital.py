from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class HospitalBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Hospital ID (server-generated).",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    name: str = Field(
        ...,
        description="Hospital name.",
        json_schema_extra={"example": "Columbia Medical Center"},
    )
    address: Optional[str] = Field(
        None,
        description="Hospital address.",
        json_schema_extra={"example": "116th St & Broadway, New York, NY 10027"},
    )
    website: Optional[str] = Field(
        None,
        description="Hospital website.",
        json_schema_extra={"example": "https://www.columbiamed.org"},
    )
    contact: Optional[str] = Field(
        None,
        description="Hospital contact phone or email.",
        json_schema_extra={"example": "+1-212-555-0100"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Columbia Medical Center",
                    "address": "116th St & Broadway, New York, NY 10027",
                    "website": "https://www.columbiamed.org",
                    "contact": "+1-212-555-0100",
                }
            ]
        }
    }

class HospitalCreate(HospitalBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "name": "St. Luke's Hospital",
                    "address": "123 Health Ave, New York, NY 10025",
                    "website": "https://www.stlukesny.org",
                    "contact": "+1-212-555-0200",
                }
            ]
        }
    }

class HospitalUpdate(BaseModel):
    """Partial update; hospital ID is taken from the path, not the body."""
    name: Optional[str] = Field(None, description="Hospital name.", json_schema_extra={"example": "New Name"})
    address: Optional[str] = Field(None, description="Hospital address.", json_schema_extra={"example": "New Address"})
    website: Optional[str] = Field(None, description="Hospital website.", json_schema_extra={"example": "https://newsite.org"})
    contact: Optional[str] = Field(None, description="Hospital contact phone or email.", json_schema_extra={"example": "+1-212-555-0300"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "New Name",
                    "address": "New Address",
                    "website": "https://newsite.org",
                    "contact": "+1-212-555-0300",
                },
                {"contact": "+1-212-555-0400"},
            ]
        }
    }

class HospitalRead(HospitalBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Columbia Medical Center",
                    "address": "116th St & Broadway, New York, NY 10027",
                    "website": "https://www.columbiamed.org",
                    "contact": "+1-212-555-0100",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }