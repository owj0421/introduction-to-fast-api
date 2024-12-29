from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from ..schemas import task as task_schema

import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()


@router.get(
    "/tasks", 
    response_model=List[task_schema.Task]
)
async def list_tasks(
    db: Session = Depends(get_db)
):
    return task_crud.get_tasks_with_done(db)


@router.post(
    "/tasks", 
    # Check: askCreateResponse를 orm모델과 연동하기 위해 어떻게 처리했는지
    response_model=task_schema.TaskCreateResponse 
) 
async def create_task(
    task_body: task_schema.TaskCreate,
    # Check: Depends를 사용하여 get_db 함수를 호출하는 이유는 무엇인가?
    db: Session = Depends(get_db)
):
    return task_crud.create_task(db, task_body)


@router.put(
    "/tasks/{task_id}", 
    response_model=task_schema.TaskCreateResponse
)
async def update_task(
    task_id: int, 
    task_body: task_schema.TaskCreate,
    db: Session = Depends(get_db),
):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_crud.update_task(db, task_body, task)


@router.delete(
    "/tasks/{task_id}",
    response_model=None,
)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_crud.delete_task(db, task)