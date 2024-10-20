from sqlalchemy.orm import Session
from typing import Optional, List, Type, TypeVar

T = TypeVar('T')

def get_by_id(db: Session, model: Type[T], id: int) -> Optional[T]:
    """Retrieve a single record by its ID."""
    return db.query(model).filter(model.id == id).first()

def get_all(db: Session, model: Type[T]) -> List[T]:
    """Retrieve all records of a model."""
    return db.query(model).all()

def exists(db: Session, model: Type[T], id: int) -> bool:
    """Check if a record exists by its ID."""
    return db.query(model).filter(model.id == id).count() > 0

def create(db: Session, model: Type[T], **kwargs) -> T:
    """Create a new record."""
    instance = model(**kwargs)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

def update(db: Session, model: Type[T], id: int, **kwargs) -> Optional[T]:
    """Update an existing record by its ID."""
    instance = db.query(model).filter(model.id == id).first()
    if instance:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
    return instance

def delete(db: Session, model: Type[T], id: int) -> bool:
    """Delete a record by its ID."""
    instance = db.query(model).filter(model.id == id).first()
    if instance:
        db.delete(instance)
        db.commit()
        return True
    return False