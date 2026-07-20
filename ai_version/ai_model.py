from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="عنوان المهمة، لا يمكن أن يكون فارغًا")


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None