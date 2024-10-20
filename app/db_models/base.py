from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    kanban_board_id = Column(Integer, ForeignKey("kanban_boards.id"), nullable=False)
    
    kanban_board = relationship("KanbanBoard", back_populates="projects")
    tickets = relationship("Ticket", back_populates="project")

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    kanban_status_id = Column(Integer, ForeignKey("kanban_statuses.id"), nullable=False)
    
    project = relationship("Project", back_populates="tickets")

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class TicketBase(BaseModel):
    project_id: int
    title: str = Field(..., max_length=255)
    description: str
    status: str = Field(..., max_length=255)
    priority: str = Field(..., max_length=255)

    @validator('title', 'status', 'priority')
    def must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Field must not be empty')
        return v

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass
