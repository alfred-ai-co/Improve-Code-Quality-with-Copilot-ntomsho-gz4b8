from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, List, Optional
from app.db_models.base import Base
from app.core.orm_utils import get_by_id, get_all, create, update, delete

T = TypeVar('T', bound=Base)

class CRUDInterface(ABC, Generic[T]):
    @abstractmethod
    def create(self, **kwargs) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Retrieve a record by its ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all records."""
        pass

    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record by its ID."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete a record by its ID."""
        pass


class BaseCRUD(Generic[T], CRUDInterface):
    """Base CRUD class for all models."""
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new record."""
        try:
            return create(self.db, self.model, **kwargs)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get(self, id: int) -> Optional[T]:
        """Retrieve a record by its ID."""
        return get_by_id(self.db, self.model, id)
    
    def get_all(self) -> List[T]:
        """Retrieve all records."""
        return get_all(self.db, self.model)
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record by its ID."""
        try:
            return update(self.db, self.model, id, **kwargs)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id: int) -> bool:
        """Delete a record by its ID."""
        try:
            return delete(self.db, self.model, id)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e


class ProjectCRUD(BaseCRUD[Project]):
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def create(self, name: str, description: str) -> Project:
        return super().create(name=name, description=description)
    
    def get(self, id: int) -> Optional[Project]:
        return super().get(id)
    
    def get_all(self) -> List[Project]:
        return super().get_all()
    
    def update(self, id: int, name: str, description: str) -> Optional[Project]:
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int) -> bool:
        return super().delete(id)


class TicketCRUD(BaseCRUD[Ticket]):
    def __init__(self, db: Session):
        super().__init__(db, Ticket)
    
    def create(self, project_id: int, title: str, description: str, status: str, priority: str) -> Ticket:
        return super().create(project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def get(self, id: int) -> Optional[Ticket]:
        return super().get(id)
    
    def get_all(self) -> List[Ticket]:
        return super().get_all()
    
    def update(self, id: int, project_id: int, title: str, description: str, status: str, priority: str) -> Optional[Ticket]:
        return super().update(id, project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def delete(self, id: int) -> bool:
        return super().delete(id)


class KanbanBoardCRUD(BaseCRUD[KanbanBoard]):
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)
        
    def create(self, name: str, description: str) -> KanbanBoard:
        return super().create(name=name, description=description)
    
    def get(self, id: int) -> Optional[KanbanBoard]:
        return super().get(id)
    
    def get_all(self) -> List[KanbanBoard]:
        return super().get_all()
    
    def update(self, id: int, name: str, description: str) -> Optional[KanbanBoard]:
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int) -> bool:
        return super().delete(id)


class KanbanStatusCRUD(BaseCRUD[KanbanStatus]):
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)
    
    def create(self, name: str, description: str, board_id: int) -> KanbanStatus:
        return super().create(name=name, description=description, board_id=board_id)
    
    def get(self, id: int) -> Optional[KanbanStatus]:
        return super().get(id)
    
    def get_all(self) -> List[KanbanStatus]:
        return super().get_all()
    
    def update(self, id: int, name: str, description: str, board_id: int) -> Optional[KanbanStatus]:
        return super().update(id, name=name, description=description, board_id=board_id)
    
    def delete(self, id: int) -> bool:
        return super().delete(id)
