from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, Generic, List, Optional
from app.db_models.base import Base
from app.db_models.interfaces import CRUDInterface

T = TypeVar('T', bound=Base)

class BaseCRUD(Generic[T], CRUDInterface[T]):
    """Base CRUD class for all models."""
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new record."""
        try:
            item = self.model(**kwargs)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def get(self, id: int) -> Optional[T]:
        """Retrieve a record by its ID."""
        return self.db.query(self.model).get(id)
    
    def get_all(self) -> List[T]:
        """Retrieve all records."""
        return self.db.query(self.model).all()
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record by its ID."""
        try:
            item = self.db.query(self.model).get(id)
            if item:
                for key, value in kwargs.items():
                    setattr(item, key, value)
                self.db.commit()
                self.db.refresh(item)
            return item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
    
    def delete(self, id: int) -> bool:
        """Delete a record by its ID."""
        try:
            item = self.db.query(self.model).get(id)
            if item:
                self.db.delete(item)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e