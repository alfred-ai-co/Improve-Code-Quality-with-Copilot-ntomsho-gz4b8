from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db_models.crud import KanbanBoardCRUD
from app.api_models.kanbanboard import KanbanBoardCreate, KanbanBoardResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=KanbanBoardResponse)
async def create_kanban_board(kanban_board: KanbanBoardCreate, db: AsyncSession = Depends(get_db)):
    kanban_board_crud = KanbanBoardCRUD(db)
    return await kanban_board_crud.create(**kanban_board.model_dump())

@router.get("/", status_code=200, response_model=list[KanbanBoardResponse])
async def get_all_kanban_boards(db: AsyncSession = Depends(get_db)):
    kanban_board_crud = KanbanBoardCRUD(db)
    return await kanban_board_crud.get_all()

@router.get("/{id}", status_code=200, response_model=KanbanBoardResponse)
async def get_kanban_board(id: int, db: AsyncSession = Depends(get_db)):
    kanban_board_crud = KanbanBoardCRUD(db)
    kanban_board = await kanban_board_crud.get(id)
    if not kanban_board:
        raise HTTPException(status_code=404, detail=f"Kanban Board with id {id} not found")
    return kanban_board

@router.put("/{id}", status_code=200, response_model=KanbanBoardResponse)
async def update_kanban_board(id: int, kanban_board: KanbanBoardCreate, db: AsyncSession = Depends(get_db)):
    kanban_board_crud = KanbanBoardCRUD(db)
    await kanban_board_crud.update(id, **kanban_board.model_dump())
    return await kanban_board_crud.get(id)

@router.delete("/{id}", status_code=204)
def delete_kanban_board(id: int, db: Session = Depends(get_db)):
    kanban_board_crud = KanbanBoardCRUD(db)
    kanban_board_crud.delete(id)
    return {"message": "Kanban Board deleted successfully"}
