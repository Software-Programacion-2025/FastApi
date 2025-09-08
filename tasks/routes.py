from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import TaskCreate, TaskOut, TaskUpdateState, TaskAssignUser
from .services import get_all_tasks, create_task, update_task_state, get_task_by_id, assign_user_to_task, unassign_user_from_task
from middlewares.auth import get_current_user
import time
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

# Dependency personalizado para logging de tareas sensibles
async def log_sensitive_operation(request: Request, current_user: dict = Depends(get_current_user)):
    """Middleware/dependency para operaciones sensibles de tareas"""
    start_time = time.time()
    user_id = current_user.get("sub", "unknown")
    user_email = current_user.get("email", "unknown")
    
    # Log antes de la operación
    logger.info(f"SENSITIVE_OP_START: User {user_id} ({user_email}) accessing {request.method} {request.url.path}")
    
    # Retornar información que puede ser usada en el endpoint
    return {
        "user_id": user_id,
        "user_email": user_email,
        "start_time": start_time,
        "operation": f"{request.method} {request.url.path}"
    }

# Dependency para logging de operaciones de lectura
async def log_read_operation(request: Request):
    """Middleware/dependency simple para operaciones de lectura"""
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"READ_OP: {request.method} {request.url.path} - IP: {client_ip}")
    return {"operation_type": "read", "timestamp": time.time()}

tasks = APIRouter()

@tasks.get('', response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_tasks(log_info: dict = Depends(log_read_operation)):
    """Obtener todas las tareas - CON middleware de logging"""
    try:
        logger.info(f"Executing get_tasks - Operation: {log_info['operation_type']}")
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
    """Obtener una tarea por ID - SIN middleware adicional"""
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
def create_task_endpoint(task: TaskCreate, log_info: dict = Depends(log_sensitive_operation)):
    """Crear una nueva tarea - CON middleware de operación sensible"""
    try:
        logger.info(f"Creating task - User: {log_info['user_ip']}, Operation: {log_info['operation_type']}")
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
