from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
import api.models.task as task_model
import api.schemas.task as task_schema

from typing import List, Tuple
from sqlalchemy import select


def create_task(
    db: Session, 
    task: task_schema.TaskCreate
):
    db_task = task_model.Task(
        title=task.title
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


def get_tasks_with_done(
    db: Session, 
) -> List[Tuple[int, str, bool]]:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            # Check: ToDO 작업이 존재 했을 때만, Done이 존재
            #        Done.id가 존재하면 True
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(
            task_model.Done
        )
    )
    
    return result.all()

def get_task(
    db: Session,
    task_id: int
) -> task_model.Task:
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    
    # Check: scalars()는 각 행에서 가져올 요소를 한개로 좁힌다.
    return result.scalars().first()


def update_task(
    db: Session,
    task_create: task_schema.TaskCreate,
    original: task_model.Task,
) -> task_model.Task:
    original.title = task_create.title
    
    db.add(original)
    db.commit()
    # the process of replacing an existing database 
    # with a copy from another environment 
    # to update the database and its data. 
    # Check: refresh가 왜 필요한가? 
    # DB에서 가져왔던 데이터를 다시 가져와서 업데이트를 해주는 것
    # Return 해야하니까.
    db.refresh(original)
    
    return original


def delete_task(
    db: Session,
    original: task_model.Task,
) -> None:
    db.delete(original)
    db.commit()