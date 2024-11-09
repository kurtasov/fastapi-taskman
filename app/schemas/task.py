from datetime import date, timedelta
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated, TypeAlias
from sqlmodel import SQLModel, Field as SQLField


def _empty_str_or_none(value: str | None) -> None:
    if value is None or value == "":
        return None
    raise ValueError("Expected empty value")


EmptyStrOrNone: TypeAlias = Annotated[None, BeforeValidator(_empty_str_or_none)]


class TaskCreate(BaseModel):
    task_description: str = Field(
        description="Описание задачи",
        max_length=300
    )
    assignee: str
    due_date: Optional[date] = Field(
        description="Крайний срок исполнения задачи. "
                    "Не допускаются даты, более ранние, "
                    "чем сегодняшняя.",
        gt=date.today() - timedelta(days=1),
        default_factory=lambda: date.today() + timedelta(days=1)
    )


class TaskRead(TaskCreate):
    task_id: int
    due_date: EmptyStrOrNone | date


class Task(SQLModel, TaskRead, table=True):
    task_id: int = SQLField(default=None, nullable=False, primary_key=True)
    due_date: date
