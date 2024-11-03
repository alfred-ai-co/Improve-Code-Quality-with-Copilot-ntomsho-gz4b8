# Project Endpoints
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db_models.crud import ProjectCRUD
from app.api_models.projects import ProjectCreate, ProjectResponse
from app.api.dependencies.sqldb import get_db

# Create a new API router for project endpoints
router = APIRouter()

@router.post("/", status_code=201, response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.

    Args:
        project (ProjectCreate): The project data to create.
        db (Session): The database session dependency.

    Returns:
        ProjectResponse: The created project.
    """
    project_crud = ProjectCRUD(db)
    return project_crud.create(**project.model_dump())

@router.get("/", status_code=200, response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    """
    Retrieve all projects.

    Args:
        db (Session): The database session dependency.

    Returns:
        list[ProjectResponse]: A list of all projects.
    """
    project_crud = ProjectCRUD(db)
    return project_crud.get_all()

@router.get("/{id}", status_code=200, response_model=ProjectResponse)
def get_project(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific project by ID.

    Args:
        id (int): The ID of the project to retrieve.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the project with the given ID is not found.

    Returns:
        ProjectResponse: The retrieved project.
    """
    project_crud = ProjectCRUD(db)
    project = project_crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
    return project

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Update a specific project by ID.

    Args:
        id (int): The ID of the project to update.
        project (ProjectCreate): The updated project data.
        db (Session): The database session dependency.

    Returns:
        ProjectResponse: The updated project.
    """
    project_crud = ProjectCRUD(db)
    project_crud.update(id, **project.model_dump())
    return project_crud.get(id)

@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    """
    Delete a specific project by ID.

    Args:
        id (int): The ID of the project to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful deletion.
    """
    project_crud = ProjectCRUD(db)
    project_crud.delete(id)
    return {"message": "Project deleted successfully"}
