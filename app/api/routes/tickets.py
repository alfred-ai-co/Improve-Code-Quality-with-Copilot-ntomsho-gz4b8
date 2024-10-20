from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db_models.crud import TicketCRUD
from app.api_models.tickets import TicketCreate, TicketResponse
from app.api.dependencies.sqldb import get_db

router = APIRouter()

@router.post("/", status_code=201, response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    return await ticket_crud.create(**ticket.model_dump())

@router.get("/", status_code=200, response_model=list[TicketResponse])
async def get_all_tickets(db: AsyncSession = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    return await ticket_crud.get_all()

@router.get("/{id}", status_code=200, response_model=TicketResponse)
async def get_ticket(id: int, db: AsyncSession = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    ticket = await ticket_crud.get(id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket with id {id} not found")
    return ticket

@router.put("/{id}", status_code=200, response_model=TicketResponse)
async def update_ticket(id: int, ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    await ticket_crud.update(id, **ticket.model_dump())
    return await ticket_crud.get(id)

@router.delete("/{id}", status_code=204)
async def delete_ticket(id: int, db: AsyncSession = Depends(get_db)):
    ticket_crud = TicketCRUD(db)
    await ticket_crud.delete(id)
