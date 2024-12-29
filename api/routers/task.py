from fastapi import APIRouter, Depends
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
async def list_tasks():
    return [task_schema.Task(id=1, title="세탁소에 맡긴 것을 찾으러 가기")]


@router.post(
    "/tasks", 
    response_model=task_schema.TaskCreateResponse
) # TaskCreateResponse를 orm모델과 연동하기 위해 어떻게 처리했는지 가서 볼 것.
async def create_task(
    task_body: task_schema.TaskCreate,
    db: Session = Depends(get_db)
):
    return task_crud.create_task(db, task_body)


@router.put(
    "/tasks/{task_id}", 
    response_model=task_schema.TaskCreateResponse
)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.model_dump())


@router.delete(
    "/tasks/{task_id}"
)
async def delete_task(task_id: int):
    return {"task": f"Task {task_id} has been deleted"}