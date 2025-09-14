from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date
from pydantic import BaseModel, Field


class EnrollmentBase(BaseModel):
    person_id: UUID = Field(
        ...,
        description="ID of the person being enrolled.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    course_id: UUID = Field(
        ...,
        description="ID of the course being enrolled in.",
        json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
    )
    enrollment_date: date = Field(
        ...,
        description="Date when the enrollment was made.",
        json_schema_extra={"example": "2025-01-15"},
    )
    status: str = Field(
        ...,
        description="Enrollment status (e.g., active, dropped, completed).",
        json_schema_extra={"example": "active"},
    )
    grade: Optional[str] = Field(
        None,
        description="Final grade received (if completed).",
        json_schema_extra={"example": "A"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "person_id": "99999999-9999-4999-8999-999999999999",
                    "course_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "enrollment_date": "2025-01-15",
                    "status": "active",
                    "grade": None,
                }
            ]
        }
    }


class EnrollmentCreate(EnrollmentBase):
    """Creation payload for an Enrollment."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "person_id": "99999999-9999-4999-8999-999999999999",
                    "course_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "enrollment_date": "2025-01-15",
                    "status": "active",
                    "grade": None,
                }
            ]
        }
    }


class EnrollmentUpdate(BaseModel):
    """Partial update for an Enrollment; supply only fields to change."""
    person_id: Optional[UUID] = Field(
        None, description="ID of the person being enrolled.", json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"}
    )
    course_id: Optional[UUID] = Field(
        None, description="ID of the course being enrolled in.", json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"}
    )
    enrollment_date: Optional[date] = Field(
        None, description="Date when the enrollment was made.", json_schema_extra={"example": "2025-01-15"}
    )
    status: Optional[str] = Field(
        None, description="Enrollment status.", json_schema_extra={"example": "completed"}
    )
    grade: Optional[str] = Field(
        None, description="Final grade received.", json_schema_extra={"example": "A"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "completed", "grade": "A"},
                {"status": "dropped"},
            ]
        }
    }


class EnrollmentRead(EnrollmentBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Enrollment ID.",
        json_schema_extra={"example": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"},
    )
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
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "person_id": "99999999-9999-4999-8999-999999999999",
                    "course_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "enrollment_date": "2025-01-15",
                    "status": "active",
                    "grade": None,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
