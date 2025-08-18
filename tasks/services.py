from .model import Task, user_task_association
from users.model import User
from config.cnx import SessionLocal
from .dto import TaskCreate, TaskUpdateState, TaskAssignUser
from sqlalchemy.orm import joinedload

def get_all_tasks():
    db = SessionLocal()
    tasks = db.query(Task).options(joinedload(Task.users)).all()
    db.close()
    return tasks

def create_task(task_data: TaskCreate):
    db = SessionLocal()
    
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == task_data.user_id, User.delete_at == None).first()
    if not user:
        db.close()
        raise ValueError("Usuario no encontrado")
    
    # Crear la tarea
    task = Task(
        title=task_data.title,
        description=task_data.description,
        state=task_data.state
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Asociar el usuario creador con la tarea
    task.users.append(user)
    db.commit()
    db.close()
    return task

def update_task_state(task_id: int, state_data: TaskUpdateState):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        db.close()
        raise ValueError("Tarea no encontrada")
    
    task.state = state_data.state  # type: ignore
    db.commit()
    db.refresh(task)
    db.close()
    return task

def get_task_by_id(task_id: int):
    db = SessionLocal()
    task = db.query(Task).options(joinedload(Task.users)).filter(Task.id == task_id).first()
    db.close()
    return task

def assign_user_to_task(task_id: int, assign_data: TaskAssignUser):
    db = SessionLocal()
    
    # Verificar que la tarea existe
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise ValueError("Tarea no encontrada")
    
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == assign_data.user_id, User.delete_at == None).first()
    if not user:
        db.close()
        raise ValueError("Usuario no encontrado")
    
    # Verificar si el usuario ya está asignado a la tarea
    if user in task.users:
        db.close()
        raise ValueError("El usuario ya está asignado a esta tarea")
    
    # Asignar el usuario a la tarea
    task.users.append(user)
    db.commit()
    db.refresh(task)
    db.close()
    return task

def unassign_user_from_task(task_id: int, user_id: str):
    db = SessionLocal()
    
    # Verificar que la tarea existe
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise ValueError("Tarea no encontrada")
    
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == user_id, User.delete_at == None).first()
    if not user:
        db.close()
        raise ValueError("Usuario no encontrado")
    
    # Verificar si el usuario está asignado a la tarea
    if user not in task.users:
        db.close()
        raise ValueError("El usuario no está asignado a esta tarea")
    
    # Desasignar el usuario de la tarea
    task.users.remove(user)
    db.commit()
    db.refresh(task)
    db.close()
    return task
