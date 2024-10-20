from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from abc import ABC, abstractmethod
from app.db_models.base import *


class CRUDInterface(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, id: int, **kwargs):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class BaseCRUD(CRUDInterface):
    """Base CRUD class for all models"""
    def __init__(self, db: Session, model=None):
        self.db = db
        self.model = model
    
    def create(self, **kwargs):
        try:
            item = self.model(**kwargs)
            self.db.add(item)
            self.db.commit()
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            # Optionally log the error
            print(f"Error creating item: {e}")
            raise

    def get(self, id: int):
        try:
            return self.db.query(self.model).get(id)
        except SQLAlchemyError as e:
            # Optionally log the error
            print(f"Error retrieving item with id {id}: {e}")
            raise

    def get_all(self):
        try:
            return self.db.query(self.model).all()
        except SQLAlchemyError as e:
            # Optionally log the error
            print(f"Error retrieving all items: {e}")
            raise

    def update(self, id: int, **kwargs):
        try:
            item = self.db.query(self.model).get(id)
            if not item:
                return None
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.commit()
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            # Optionally log the error
            print(f"Error updating item with id {id}: {e}")
            raise

    def delete(self, id: int):
        try:
            item = self.db.query(self.model).get(id)
            if not item:
                return None
            self.db.delete(item)
            self.db.commit()
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            # Optionally log the error
            print(f"Error deleting item with id {id}: {e}")
            raise


class ProjectCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def create(self, name: str, description: str):
        return super().create(name=name, description=description)
    
    def get(self, id: int):
        return super().get(id)
    
    def get_all(self):
        return super().get_all()
    
    def update(self, id: int, name: str, description: str):
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int):
        return super().delete(id)


class TicketCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Ticket)
    
    def create(self, project_id: int, title: str, description: str, status: str, priority: str):
        return super().create(project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def get(self, id: int):
        return super().get(id)
    
    def get_all(self):
        return super().get_all()
    
    def update(self, id: int, project_id: int, title: str, description: str, status: str, priority: str):
        return super().update(id, project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def delete(self, id: int):
        return super().delete(id)


class KanbanBoardCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)
        
    def create(self, name: str, description: str):
        return super().create(name=name, description=description)
    
    def get(self, id: int):
        return super().get(id)
    
    def get_all(self):
        return super().get_all()
    
    def update(self, id: int, name: str, description: str) -> KanbanBoard:
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int) -> None:
        return super().delete(id)


class KanbanStatusCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)
    
    def create(self, name: str, description: str, board_id: int):
        return super().create(name=name, description=description, board_id=board_id)
    
    def get(self, id: int):
        return super().get(id)
    
    def get_all(self):
        return super().get_all()
    
    def update(self, id: int, name: str, description: str, board_id: int):
        return super().update(id, name=name, description=description, board_id=board_id)
    
    def delete(self, id: int):
        return super().delete(id)