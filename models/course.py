from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    course_code: str = Field(
        ...,
        description="Course code (e.g., COMS4153, MATH101).",
        json_schema_extra={"example": "COMS4153"},
    )
    title: str = Field(
        ...,
        description="Course title.",
        json_schema_extra={"example": "Cloud Computing"},
    )
    description: Optional[str] = Field(
        None,
        description="Course description.",
        json_schema_extra={"example": "Introduction to cloud computing concepts and technologies."},
    )
    credits: int = Field(
        ...,
        description="Number of credit hours.",
        json_schema_extra={"example": 3},
    )
    department: str = Field(
        ...,
        description="Academic department offering the course.",
        json_schema_extra={"example": "Computer Science"},
    )
    semester: str = Field(
        ...,
        description="Semester when course is offered (e.g., Fall2024, Spring2025).",
        json_schema_extra={"example": "Fall2024"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS4153",
                    "title": "Cloud Computing",
                    "description": "Introduction to cloud computing concepts and technologies.",
                    "credits": 3,
                    "department": "Computer Science",
                    "semester": "Fall2024",
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    """Creation payload for a Course."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "MATH101",
                    "title": "Calculus I",
                    "description": "Introduction to differential and integral calculus.",
                    "credits": 4,
                    "department": "Mathematics",
                    "semester": "Spring2025",
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update for a Course; supply only fields to change."""
    course_code: Optional[str] = Field(
        None, description="Course code.", json_schema_extra={"example": "COMS4153"}
    )
    title: Optional[str] = Field(
        None, description="Course title.", json_schema_extra={"example": "Advanced Cloud Computing"}
    )
    description: Optional[str] = Field(
        None, description="Course description.", json_schema_extra={"example": "Advanced topics in cloud computing."}
    )
    credits: Optional[int] = Field(
        None, description="Number of credit hours.", json_schema_extra={"example": 4}
    )
    department: Optional[str] = Field(
        None, description="Academic department.", json_schema_extra={"example": "Computer Science"}
    )
    semester: Optional[str] = Field(
        None, description="Semester when course is offered.", json_schema_extra={"example": "Spring2025"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Advanced Cloud Computing", "credits": 4},
                {"semester": "Spring2025"},
            ]
        }
    }


class CourseRead(CourseBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Course ID.",
        json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
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
                    "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "course_code": "COMS4153",
                    "title": "Cloud Computing",
                    "description": "Introduction to cloud computing concepts and technologies.",
                    "credits": 3,
                    "department": "Computer Science",
                    "semester": "Fall2024",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
