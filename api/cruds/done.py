from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

import api.models.task as task_model


def get_done(
    db: Session,
    task_id: int,
) -> task_model.Done | None: # task_id에 해당하지 않는 것이 있을수도 있으므로.
    result = db.execute(
        select(
            task_model.Done
        ).filter(
            task_model.Done.id == task_id
        )
    )
    
    return result.scalars().first()
    

def create_done(
    db: Session,
    task_id: int,
) -> task_model.Done:
    done = task_model.Done(id=task_id)
    db.add(done)
    db.commit()
    db.refresh(done)
    
    return done
    

def delete_done(
    db: Session,
    original: task_model.Done,
) -> None:
    db.delete(original)
    db.commit()