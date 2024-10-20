# Project Endpoints
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db_models.crud import ProjectCRUD
from app.api_models.projects import ProjectCreate, ProjectResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    return await project_crud.create(**project.model_dump())

@router.get("/", status_code=200, response_model=list[ProjectResponse])
async def get_all_projects(db: AsyncSession = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    return await project_crud.get_all()

@router.get("/{id}", status_code=200, response_model=ProjectResponse)
async def get_project(id: int, db: AsyncSession = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    project = await project_crud.get(id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
    return project

@router.put("/{id}", status_code=200, response_model=ProjectResponse)
async def update_project(id: int, project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    await project_crud.update(id, **project.model_dump())
    return await project_crud.get(id)

@router.delete("/{id}", status_code=204)
async def delete_project(id: int, db: AsyncSession = Depends(get_db)):
    project_crud = ProjectCRUD(db)
    await project_crud.delete(id)
