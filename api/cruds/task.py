from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.task as task_schema

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