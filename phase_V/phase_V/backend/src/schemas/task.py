"""
Pydantic schemas for Task CRUD operations.

All schemas use Pydantic v2 syntax with ConfigDict.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecurrenceEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional task description"
    )
    priority: PriorityEnum = Field(
        default=PriorityEnum.MEDIUM,
        description="Task priority (low, medium, high)"
    )
    tags: List[str] = Field(
        default=[],
        description="List of tags for the task"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Due date for the task"
    )
    recurrence: Optional[RecurrenceEnum] = Field(
        default=None,
        description="Recurrence pattern for the task (daily, weekly, monthly)"
    )

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional - only provided fields will be updated.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Task description"
    )
    completed: bool | None = Field(
        default=None,
        description="Completion status"
    )
    priority: PriorityEnum | None = Field(
        default=None,
        description="Task priority (low, medium, high)"
    )
    tags: List[str] | None = Field(
        default=None,
        description="List of tags for the task"
    )
    due_date: Optional[datetime] | None = Field(
        default=None,
        description="Due date for the task"
    )
    recurrence: Optional[RecurrenceEnum] | None = Field(
        default=None,
        description="Recurrence pattern for the task (daily, weekly, monthly)"
    )

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    """
    Schema for task response.

    CONSTITUTION COMPLIANCE (Article III):
    - user_id: UUID type (native PostgreSQL UUID), NOT int
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Task ID (integer)")
    user_id: UUID = Field(..., description="Native UUID of task owner")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    completed: bool = Field(..., description="Completion status")
    priority: PriorityEnum = Field(..., description="Task priority")
    tags: List[str] = Field(..., description="List of tags for the task")
    due_date: Optional[datetime] = Field(..., description="Due date for the task")
    recurrence: Optional[RecurrenceEnum] | None = Field(..., description="Recurrence pattern for the task")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""

    model_config = ConfigDict(from_attributes=True)

    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
