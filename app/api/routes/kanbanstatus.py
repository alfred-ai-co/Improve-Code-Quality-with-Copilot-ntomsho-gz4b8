from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db_models.crud import KanbanStatusCRUD
from app.api_models.kanbanstatus import KanbanStatusCreate, KanbanStatusResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=KanbanStatusResponse)
async def create_kanban_status(kanban_status: KanbanStatusCreate, db: AsyncSession = Depends(get_db)):
    kanban_status_crud = KanbanStatusCRUD(db)
    return await kanban_status_crud.create(**kanban_status.model_dump())

@router.get("/", status_code=200, response_model=list[KanbanStatusResponse])
async def get_all_kanban_statuses(db: AsyncSession = Depends(get_db)):
    kanban_status_crud = KanbanStatusCRUD(db)
    return await kanban_status_crud.get_all()

@router.get("/{id}", status_code=200, response_model=KanbanStatusResponse)
async def get_kanban_status(id: int, db: AsyncSession = Depends(get_db)):
    kanban_status_crud = KanbanStatusCRUD(db)
    kanban_status = await kanban_status_crud.get(id)
    if not kanban_status:
        raise HTTPException(status_code=404, detail=f"Kanban Status with id {id} not found")
    return kanban_status

@router.put("/{id}", status_code=200, response_model=KanbanStatusResponse)
async def update_kanban_status(id: int, kanban_status: KanbanStatusCreate, db: AsyncSession = Depends(get_db)):
    kanban_status_crud = KanbanStatusCRUD(db)
    await kanban_status_crud.update(id, **kanban_status.model_dump())
    return await kanban_status_crud.get(id)

@router.delete("/{id}", status_code=204)
async def delete_kanban_status(id: int, db: AsyncSession = Depends(get_db)):
    kanban_status_crud = KanbanStatusCRUD(db)
    await kanban_status_crud.delete(id)
