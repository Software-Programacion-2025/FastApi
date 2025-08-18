from fastapi import APIRouter, HTTPException
from typing import List
from .dto import TaskCreate, TaskOut, TaskUpdateState, TaskAssignUser
from .services import get_all_tasks, create_task, update_task_state, get_task_by_id, assign_user_to_task, unassign_user_from_task

tasks = APIRouter()

@tasks.get('', response_model=List[TaskOut], status_code=200)
def get_tasks():
    return get_all_tasks()

@tasks.get('/{task_id}', response_model=TaskOut, status_code=200)
def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@tasks.post('', response_model=TaskOut, status_code=201)
def post_task(task: TaskCreate):
    try:
        return create_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@tasks.patch('/{task_id}/state', response_model=TaskOut, status_code=200)
def update_task_status(task_id: int, state_data: TaskUpdateState):
    """Endpoint para cambiar el estado de una tarea"""
    try:
        return update_task_state(task_id, state_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@tasks.post('/{task_id}/assign', response_model=TaskOut, status_code=200)
def assign_user(task_id: int, assign_data: TaskAssignUser):
    """Endpoint para asignar un usuario a una tarea existente"""
    try:
        return assign_user_to_task(task_id, assign_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@tasks.delete('/{task_id}/assign/{user_id}', response_model=TaskOut, status_code=200)
def unassign_user(task_id: int, user_id: str):
    """Endpoint para desasignar un usuario de una tarea"""
    try:
        return unassign_user_from_task(task_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
