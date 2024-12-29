from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks/{task_id}/done")
async def mark_task_as_done(task_id: int):
    pass


@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done(task_id: int):
    pass