#!/usr/bin/env python3
"""
Seeder principal para cargar todos los datos básicos del sistema
Ejecuta todos los seeders en el orden correcto para mantener la integridad referencial
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal, engine
from config.basemodel import Base
import logging

# Importar TODOS los modelos para asegurar que las tablas se registren
from roles.model import Rol
from users.model import User
from tasks.model import Task
from permisos.model import Permiso
from config.associations import rol_permiso_association, user_task_association

# Importar utilidades de tablas
from table_utils import create_foreign_keys, verify_tables

# Importar funciones de seeding
from seed_roles import seed_roles, create_roles_table
from seed_usuarios import seed_usuarios, create_users_table  
from seed_permisos import seed_permisos, create_permissions_table
from seed_rol_permisos import seed_rol_permisos
from seed_tasks import seed_tasks, create_tasks_table

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_all_tables():
    """Crear todas las tablas del sistema"""
    try:
        print("=== Creando/Verificando todas las tablas ===")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas base creadas/verificadas exitosamente")
        print("✓ Tablas base creadas/verificadas exitosamente")
        
        # Verificar y crear foreign keys
        print("=== Verificando integridad de tablas ===")
        if verify_tables():
            create_foreign_keys()
        
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        print(f"✗ Error al crear tablas: {e}")
        raise

def run_all_seeders():
    """Ejecutar todos los seeders en el orden correcto"""
    
    print("\n" + "="*60)
    print("🌱 INICIANDO SEEDING COMPLETO DEL SISTEMA")
    print("="*60)
    
    try:
        # 1. Crear todas las tablas primero
        create_all_tables()
        
        # 2. Cargar roles (base para usuarios y permisos)
        print("\n" + "="*40)
        print("📋 PASO 1: Cargando Roles")
        print("="*40)
        seed_roles()
        
        # 3. Cargar usuarios (depende de roles)
        print("\n" + "="*40)
        print("👥 PASO 2: Cargando Usuarios")
        print("="*40)
        seed_usuarios()
        
        # 4. Cargar permisos (independiente)
        print("\n" + "="*40)
        print("🔐 PASO 3: Cargando Permisos")
        print("="*40)
        seed_permisos()
        
        # 5. Asignar permisos a roles (depende de roles y permisos)
        print("\n" + "="*40)
        print("🔗 PASO 4: Asignando Permisos a Roles")
        print("="*40)
        seed_rol_permisos()
        
        # 6. Cargar tasks (independiente)
        print("\n" + "="*40)
        print("� PASO 5: Cargando Tasks")
        print("="*40)
        seed_tasks()
        
        print("\n" + "="*60)
        print("✅ SEEDING COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("🎉 El sistema está listo para usar!")
        print("\n📋 Datos cargados:")
        print("   - Roles del sistema (Administrador, Gerente, Empleado, Cajero)")
        print("   - Usuarios de ejemplo para cada rol")
        print("   - Permisos detallados por módulo")
        print("   - Asignaciones de permisos por rol")
        print("   - Tareas de ejemplo para el sistema")
        print("\n🔑 Credenciales por defecto:")
        print("   - admin / admin123 (Administrador)")
        print("   - gerente01 / gerente123 (Gerente)")
        print("   - empleado01 / emp123 (Empleado)")
        print("   - cajero01 / cajero123 (Cajero)")
        
        logger.info("🎉 Seeding completo exitoso")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE EL SEEDING: {e}")
        logger.error(f"❌ Error durante seeding completo: {e}")
        raise

def run_individual_seeder(seeder_name):
    """Ejecutar un seeder individual"""
    
    seeders = {
        'roles': {
            'function': seed_roles,
            'description': 'Cargar roles del sistema'
        },
        'usuarios': {
            'function': seed_usuarios,
            'description': 'Cargar usuarios de ejemplo'
        },
        'permisos': {
            'function': seed_permisos,
            'description': 'Cargar permisos del sistema'
        },
        'rol-permisos': {
            'function': seed_rol_permisos,
            'description': 'Asignar permisos a roles'
        },
        'tasks': {
            'function': seed_tasks,
            'description': 'Cargar tareas de ejemplo'
        }
    }
    
    if seeder_name not in seeders:
        print(f"❌ Seeder '{seeder_name}' no encontrado")
        print("Seeders disponibles:")
        for name, info in seeders.items():
            print(f"   - {name}: {info['description']}")
        return
    
    print(f"\n🌱 Ejecutando seeder: {seeder_name}")
    print(f"📝 Descripción: {seeders[seeder_name]['description']}")
    print("-" * 40)
    
    try:
        create_all_tables()
        seeders[seeder_name]['function']()
        print(f"✅ Seeder '{seeder_name}' ejecutado exitosamente")
    except Exception as e:
        print(f"❌ Error en seeder '{seeder_name}': {e}")
        raise

def show_help():
    """Mostrar ayuda de uso"""
    print("""
🌱 SEEDER PRINCIPAL - SISTEMA DE CAFETERÍA

USO:
    python seed_main.py [comando]

COMANDOS:
    all                    Ejecutar todos los seeders (recomendado)
    roles                  Cargar solo roles
    usuarios               Cargar solo usuarios  
    permisos               Cargar solo permisos
    rol-permisos           Asignar permisos a roles
    tasks                  Cargar tareas de ejemplo
    help                   Mostrar esta ayuda

EJEMPLOS:
    python seed_main.py all           # Seeding completo
    python seed_main.py roles         # Solo roles
    python seed_main.py permisos      # Solo permisos

ORDEN RECOMENDADO (para ejecución individual):
    1. roles
    2. usuarios
    3. permisos
    4. rol-permisos

NOTA: El comando 'all' ejecuta automáticamente todos los seeders
      en el orden correcto y es la opción recomendada.
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'all':
            run_all_seeders()
        elif command == 'help':
            show_help()
        else:
            run_individual_seeder(command)
    else:
        # Sin argumentos, ejecutar todo por defecto
        response = input("¿Desea ejecutar el seeding completo? (s/N): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            run_all_seeders()
        else:
            show_help()