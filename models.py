from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The title of the task cannot be empty")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None