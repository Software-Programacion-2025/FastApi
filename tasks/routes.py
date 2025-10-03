from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import TaskCreate, TaskOut, TaskUpdateState, TaskUpdate, TaskAssignUser
from .services import get_all_tasks, get_tasks_by_user, create_task, update_task_state, update_task_full, get_task_by_id, assign_user_to_task, unassign_user_from_task
from middlewares.auth import get_current_user
import time
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

# Dependency personalizado para logging de tareas sensibles
async def log_sensitive_operation(request: Request, current_user: dict = Depends(get_current_user)):
    """Middleware/dependency para operaciones sensibles de tareas"""
    start_time = time.time()
    
    # Log de la operación
    operation = f"{request.method} {request.url.path}"
    
    return {
        "user_id": current_user["user_id"],
        "user_email": current_user["sub"], 
        "operation": operation,
        "start_time": start_time
    }

# Dependency para logging de operaciones de lectura
async def log_read_operation(request: Request):
    """Middleware/dependency simple para operaciones de lectura"""
    start_time = time.time()
    operation = f"{request.method} {request.url.path}"
    
    return {
        "operation": operation,
        "start_time": start_time
    }

tasks = APIRouter()

@tasks.get('', response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_tasks(log_info: dict = Depends(log_read_operation)):
    """Obtener todas las tareas - CON middleware de lectura"""
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
def get_task(task_id: int, log_info: dict = Depends(log_read_operation)):
    """Obtener una tarea por ID - CON middleware de lectura"""
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
                detail="Tarea no encontrada"
            )
        
        return task
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
            detail="Error interno del servidor al obtener la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener la tarea"
        )

@tasks.get('/user/{user_id}', response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_user_tasks(user_id: str, log_info: dict = Depends(log_read_operation)):
    """Obtener todas las tareas asignadas a un usuario específico"""
    try:
        
        if not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario no puede estar vacío"
            )
        
        tasks = get_tasks_by_user(user_id)
        return tasks
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tareas del usuario {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener las tareas del usuario"
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener tareas del usuario {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener las tareas del usuario"
        )

@tasks.post('', response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task: TaskCreate, log_info: dict = Depends(log_sensitive_operation)):
    """Crear una nueva tarea - CON middleware de operación sensible"""
    try:
        return create_task(task)
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

@tasks.put('/{task_id}', response_model=TaskOut, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskUpdateState):
    """Actualizar una tarea - SIN middleware adicional"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        
        return update_task_state(task_id, task)
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
            detail="Error interno del servidor al actualizar la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar la tarea"
        )

@tasks.patch('/{task_id}', response_model=TaskOut, status_code=status.HTTP_200_OK)
def update_task_full_endpoint(task_id: int, task: TaskUpdate, log_info: dict = Depends(log_sensitive_operation)):
    """Actualizar una tarea completa (título, descripción, estado) - CON middleware de operación sensible"""
    try:
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de tarea debe ser un número positivo"
            )
        return update_task_full(task_id, task)
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
            detail="Error interno del servidor al actualizar la tarea"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar la tarea"
        )

@tasks.post('/{task_id}/assign', response_model=TaskOut, status_code=status.HTTP_200_OK)
def assign_user(task_id: int, assign_data: TaskAssignUser, log_info: dict = Depends(log_sensitive_operation)):
    """Endpoint para asignar un usuario a una tarea existente - CON middleware de operación sensible"""
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
def unassign_user(task_id: int, user_id: str, log_info: dict = Depends(log_sensitive_operation)):
    """Endpoint para desasignar un usuario de una tarea - CON middleware de operación sensible"""
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