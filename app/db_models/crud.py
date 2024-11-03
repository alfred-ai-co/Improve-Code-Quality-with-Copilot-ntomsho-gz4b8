from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from app.db_models.base import *


class CRUDInterface(ABC):
    @abstractmethod
    def create(self, **kwargs):
        """
        Create a new record in the database.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The created record.
        """
        pass

    @abstractmethod
    def get(self, id: int):
        """
        Retrieve a record by its ID.

        Args:
            id (int): The ID of the record to retrieve.

        Returns:
            The record with the specified ID, or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all records from the database.

        Returns:
            list: A list of all records.
        """
        pass

    @abstractmethod
    def update(self, id: int, **kwargs):
        """
        Update an existing record in the database.

        Args:
            id (int): The unique identifier of the record to update.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The updated record.
        """
        pass

    @abstractmethod
    def delete(self, id: int):
        """
        Delete a record from the database by its ID.

        Args:
            id (int): The unique identifier of the record to be deleted.

        Returns:
            The result of the deletion operation.
        """
        pass


class BaseCRUD(CRUDInterface):
    """Base CRUD class for all models"""
    def __init__(self, db: Session, model=None):
        self.db = db
        self.model = model
    
    def create(self, **kwargs):
        """
        Create a new record in the database.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The created record.
        """
        item = self.model(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, id: int):
        """
        Retrieve a record by its ID.

        Args:
            id (int): The ID of the record to retrieve.

        Returns:
            The record with the specified ID, or None if not found.
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        """
        Retrieve all records from the database.

        Returns:
            list: A list of all records.
        """
        return self.db.query(self.model).all()

    def update(self, id: int, **kwargs):
        """
        Update an existing record in the database.

        Args:
            id (int): The unique identifier of the record to update.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The updated record.
        """
        item = self.get(id)
        for key, value in kwargs.items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: int):
        """
        Delete a record from the database by its ID.

        Args:
            id (int): The unique identifier of the record to be deleted.

        Returns:
            The result of the deletion operation.
        """
        item = self.get(id)
        self.db.delete(item)
        self.db.commit()


class ProjectCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def create(self, name: str, description: str):
        """
        Create a new project.

        Args:
            name (str): The name of the project.
            description (str): The description of the project.

        Returns:
            Project: The created project instance.
        """
        return super().create(name=name, description=description)
    
    def get(self, id: int):
        """
        Retrieve an object by its ID.

        Args:
            id (int): The ID of the object to retrieve.

        Returns:
            The object with the specified ID, or None if not found.
        """
        return super().get(id)
    
    def get_all(self):
        """
        Retrieve all records from the database.

        Returns:
            list: A list of all records.
        """
        return super().get_all()
    
    def update(self, id: int, name: str, description: str):
        """
        Update an existing record in the database.

        Args:
            id (int): The unique identifier of the record to update.
            name (str): The new name for the record.
            description (str): The new description for the record.

        Returns:
            The updated record.
        """
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int):
        """
        Delete an entry from the database by its ID.

        Args:
            id (int): The unique identifier of the entry to be deleted.

        Returns:
            The result of the deletion operation, as defined by the superclass.
        """
        return super().delete(id)


class TicketCRUD(BaseCRUD):
    """
    CRUD operations for Ticket model.
    Args:
        db (Session): SQLAlchemy session object.
    Methods:
        create(project_id: int, title: str, description: str, status: str, priority: str):
            Creates a new ticket with the given details.
        get(id: int):
            Retrieves a ticket by its ID.
        get_all():
            Retrieves all tickets.
        update(id: int, project_id: int, title: str, description: str, status: str, priority: str):
            Updates an existing ticket with the given details.
        delete(id: int):
            Deletes a ticket by its ID.
    """
    def __init__(self, db: Session):
        super().__init__(db, Ticket)
    
    def create(self, project_id: int, title: str, description: str, status: str, priority: str):
        """
        Create a new ticket.

        Args:
            project_id (int): The ID of the project the ticket belongs to.
            title (str): The title of the ticket.
            description (str): The description of the ticket.
            status (str): The status of the ticket.
            priority (str): The priority of the ticket.

        Returns:
            Ticket: The created ticket instance.
        """
        return super().create(project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def get(self, id: int):
        """
        Retrieve a ticket by its ID.

        Args:
            id (int): The ID of the ticket to retrieve.

        Returns:
            The ticket with the specified ID, or None if not found.
        """
        return super().get(id)
    
    def get_all(self):
        """
        Retrieve all tickets from the database.

        Returns:
            list: A list of all tickets.
        """
        return super().get_all()
    
    def update(self, id: int, project_id: int, title: str, description: str, status: str, priority: str):
        """
        Update an existing ticket in the database.

        Args:
            id (int): The unique identifier of the ticket to update.
            project_id (int): The ID of the project the ticket belongs to.
            title (str): The new title for the ticket.
            description (str): The new description for the ticket.
            status (str): The new status for the ticket.
            priority (str): The new priority for the ticket.

        Returns:
            The updated ticket.
        """
        return super().update(id, project_id=project_id, title=title, description=description, status=status, priority=priority)
    
    def delete(self, id: int):
        """
        Delete a ticket from the database by its ID.

        Args:
            id (int): The unique identifier of the ticket to be deleted.

        Returns:
            The result of the deletion operation.
        """
        return super().delete(id)


class KanbanBoardCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanBoard)
        
    def create(self, name: str, description: str):
        """
        Create a new Kanban board.

        Args:
            name (str): The name of the Kanban board.
            description (str): The description of the Kanban board.

        Returns:
            KanbanBoard: The created Kanban board instance.
        """
        return super().create(name=name, description=description)
    
    def get(self, id: int):
        """
        Retrieve a Kanban board by its ID.

        Args:
            id (int): The ID of the Kanban board to retrieve.

        Returns:
            The Kanban board with the specified ID, or None if not found.
        """
        return super().get(id)
    
    def get_all(self):
        """
        Retrieve all Kanban boards from the database.

        Returns:
            list: A list of all Kanban boards.
        """
        return super().get_all()
    
    def update(self, id: int, name: str, description: str) -> KanbanBoard:
        """
        Update an existing Kanban board in the database.

        Args:
            id (int): The unique identifier of the Kanban board to update.
            name (str): The new name for the Kanban board.
            description (str): The new description for the Kanban board.

        Returns:
            The updated Kanban board.
        """
        return super().update(id, name=name, description=description)
    
    def delete(self, id: int) -> None:
        """
        Delete a Kanban board from the database by its ID.

        Args:
            id (int): The unique identifier of the Kanban board to be deleted.

        Returns:
            The result of the deletion operation.
        """
        return super().delete(id)


class KanbanStatusCRUD(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, KanbanStatus)
    
    def create(self, name: str, description: str, board_id: int):
        """
        Create a new Kanban status.

        Args:
            name (str): The name of the Kanban status.
            description (str): The description of the Kanban status.
            board_id (int): The ID of the board the status belongs to.

        Returns:
            KanbanStatus: The created Kanban status instance.
        """
        return super().create(name=name, description=description, board_id=board_id)
    
    def get(self, id: int):
        """
        Retrieve a Kanban status by its ID.

        Args:
            id (int): The ID of the Kanban status to retrieve.

        Returns:
            The Kanban status with the specified ID, or None if not found.
        """
        return super().get(id)
    
    def get_all(self):
        """
        Retrieve all Kanban statuses from the database.

        Returns:
            list: A list of all Kanban statuses.
        """
        return super().get_all()
    
    def update(self, id: int, name: str, description: str, board_id: int):
        """
        Update an existing Kanban status in the database.

        Args:
            id (int): The unique identifier of the Kanban status to update.
            name (str): The new name for the Kanban status.
            description (str): The new description for the Kanban status.
            board_id (int): The ID of the board the status belongs to.

        Returns:
            The updated Kanban status.
        """
        return super().update(id, name=name, description=description, board_id=board_id)
    
    def delete(self, id: int):
        """
        Delete a Kanban status from the database by its ID.

        Args:
            id (int): The unique identifier of the Kanban status to be deleted.

        Returns:
            The result of the deletion operation.
        """
        return super().delete(id)