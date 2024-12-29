from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.db import get_db

router = APIRouter()


@router.put(
    "/tasks/{task_id}/done",
    response_model=done_schema.DoneResponse
)
async def mark_task_as_done(
    task_id: int,
    # db: Session = Depends(get_db)
    db: AsyncSession = Depends(get_db),
):
    # done = done_crud.get_done(db, task_id)
    done = await done_crud.get_done(db, task_id)
    if done:
        raise HTTPException(status_code=400, detail="Task is already done")
    
    # return done_crud.create_done(db, task_id)
    return await done_crud.create_done(db, task_id)


@router.delete(
    "/tasks/{task_id}/done",
    response_model=None
)
async def unmark_task_as_done(
    task_id: int,
    # db: Session = Depends(get_db)
    db: AsyncSession = Depends(get_db),
):
    # done = done_crud.get_done(db, task_id)
    done = await done_crud.get_done(db, task_id)
    if not done:
        raise HTTPException(status_code=400, detail="Task is not done")
    
    # return done_crud.delete_done(db, done)
    return await done_crud.delete_done(db, done)