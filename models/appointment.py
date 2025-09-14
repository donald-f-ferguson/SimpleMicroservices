from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints

# Import UNIType from person.py for consistency
UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]

class AppointmentBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Appointment ID (server-generated).",
        json_schema_extra={"example": "789e8400-e29b-41d4-a716-446655440000"},
    )
    person_id: UNIType = Field(
        ...,
        description="UNI of the person for this appointment.",
        json_schema_extra={"example": "abc1234"},
    )
    hospital_id: Optional[UUID] = Field(
        None,
        description="ID of the hospital for this appointment.",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    appointment_time: datetime = Field(
        ...,
        description="Date and time of the appointment (UTC).",
        json_schema_extra={"example": "2025-09-12T15:00:00Z"},
    )
    description: Optional[str] = Field(
        None,
        description="Description or purpose of the appointment.",
        json_schema_extra={"example": "Annual checkup"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "789e8400-e29b-41d4-a716-446655440000",
                    "person_id": "abc1234",
                    "hospital_id": "123e4567-e89b-12d3-a456-426614174000",
                    "appointment_time": "2025-09-12T15:00:00Z",
                    "description": "Annual checkup",
                }
            ]
        }
    }

class AppointmentCreate(AppointmentBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "88888888-8888-4888-8888-888888888888",
                    "person_id": "xy123",
                    "hospital_id": "123e4567-e89b-12d3-a456-426614174000",
                    "appointment_time": "2025-10-01T09:00:00Z",
                    "description": "Dental cleaning",
                }
            ]
        }
    }

class AppointmentUpdate(BaseModel):
    """Partial update; appointment ID is taken from the path, not the body."""
    person_id: Optional[UNIType] = Field(
        None, description="UNI of the person.", json_schema_extra={"example": "xy123"}
    )
    hospital_id: Optional[UUID] = Field(
        None, description="ID of the hospital.", json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"}
    )
    appointment_time: Optional[datetime] = Field(
        None, description="Date and time of the appointment.", json_schema_extra={"example": "2025-10-01T09:00:00Z"}
    )
    description: Optional[str] = Field(
        None, description="Description or purpose.", json_schema_extra={"example": "Dental cleaning"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "appointment_time": "2025-10-01T09:00:00Z",
                    "description": "Dental cleaning",
                },
                {"description": "Updated appointment"},
            ]
        }
    }

class AppointmentRead(AppointmentBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-09-12T12:00:00Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-09-12T12:30:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "789e8400-e29b-41d4-a716-446655440000",
                    "person_id": "abc1234",
                    "hospital_id": "123e4567-e89b-12d3-a456-426614174000",
                    "appointment_time": "2025-09-12T15:00:00Z",
                    "description": "Annual checkup",
                    "created_at": "2025-09-12T12:00:00Z",
                    "updated_at": "2025-09-12T12:30:00Z",
                }
            ]
        }
    }