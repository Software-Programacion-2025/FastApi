from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import TaskCreate, TaskOut, TaskUpdateState, TaskAssignUser
from .services import get_all_tasks, create_task, update_task_state, get_task_by_id, assign_user_to_task, unassign_user_from_task

tasks = APIRouter()

@tasks.get('', response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_tasks():
    """Obtener todas las tareas"""
    try:
        return get_all_tasks()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener las tareas"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener las tareas"
        )

@tasks.get('/{task_id}', response_model=TaskOut, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    """Obtener una tarea por ID"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        
        task = get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        return task
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener la tarea"
        )

@tasks.post('', response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def post_task(task: TaskCreate):
    """Crear una nueva tarea"""
    try:
        if not task.title or not task.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título de la tarea es requerido"
            )
        
        return create_task(task)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de integridad de datos al crear la tarea"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear la tarea"
        )

@tasks.patch('/{task_id}/state', response_model=TaskOut, status_code=status.HTTP_200_OK)
def update_task_status(task_id: int, state_data: TaskUpdateState):
    """Endpoint para cambiar el estado de una tarea"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        
        valid_states = ['pending', 'in_progress', 'completed', 'cancelled']
        if state_data.state not in valid_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Estados válidos: {', '.join(valid_states)}"
            )
        
        return update_task_state(task_id, state_data)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al actualizar la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar la tarea"
        )

@tasks.post('/{task_id}/assign', response_model=TaskOut, status_code=status.HTTP_200_OK)
def assign_user(task_id: int, assign_data: TaskAssignUser):
    """Endpoint para asignar un usuario a una tarea existente"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        
        if not assign_data.user_id or not assign_data.user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        return assign_user_to_task(task_id, assign_data)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya está asignado a esta tarea"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al asignar usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al asignar usuario"
        )

@tasks.delete('/{task_id}/assign/{user_id}', response_model=TaskOut, status_code=status.HTTP_200_OK)
def unassign_user(task_id: int, user_id: str):
    """Endpoint para desasignar un usuario de una tarea"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        return unassign_user_from_task(task_id, user_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al desasignar usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al desasignar usuario"
        )
