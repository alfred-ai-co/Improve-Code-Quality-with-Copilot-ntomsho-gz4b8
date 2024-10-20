from pydantic import BaseModel, Field, validator
from typing import Optional
import datetime

class KanbanBoardBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

class KanbanStatusBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

class KanbanBoardCreate(KanbanBoardBase):
    pass

class KanbanStatusCreate(KanbanStatusBase):
    pass

class KanbanBoardUpdate(KanbanBoardBase):
    pass

class KanbanStatusUpdate(KanbanStatusBase):
    pass