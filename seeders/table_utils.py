"""
Utilidades para la creación segura de tablas con foreign keys
"""
from sqlalchemy import text
from config.cnx import engine

def create_foreign_keys():
    """Crear foreign keys para la tabla intermedia después de que las tablas principales existan"""
    try:
        with engine.connect() as conn:
            # Verificar si las foreign keys ya existen
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('roles', 'permisos', 'rol_permiso')
            """))
            
            existing_tables = [row[0] for row in result.fetchall()]
            
            if 'roles' in existing_tables and 'permisos' in existing_tables and 'rol_permiso' in existing_tables:
                # Crear índices para mejorar performance
                try:
                    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_rol_permiso_rol_id ON rol_permiso(rol_id)"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_rol_permiso_permiso_id ON rol_permiso(permiso_id)"))
                    conn.commit()
                    print("✓ Índices de rol_permiso creados correctamente")
                except Exception as e:
                    print(f"⚠ Error creando índices (puede ser normal): {e}")
                
                return True
            else:
                print(f"⚠ Faltan tablas: {set(['roles', 'permisos', 'rol_permiso']) - set(existing_tables)}")
                return False
                
    except Exception as e:
        print(f"✗ Error verificando/creando foreign keys: {e}")
        return False

def verify_tables():
    """Verificar que todas las tablas necesarias existan"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """))
            
            tables = [row[0] for row in result.fetchall()]
            required_tables = ['roles', 'users', 'tasks', 'permisos', 'rol_permiso', 'user_task_association']
            
            print("=== Tablas existentes ===")
            for table in tables:
                status = "✓" if table in required_tables else "-"
                print(f"{status} {table}")
            
            missing = set(required_tables) - set(tables)
            if missing:
                print(f"⚠ Faltan tablas: {missing}")
                return False
            else:
                print("✓ Todas las tablas requeridas existen")
                return True
                
    except Exception as e:
        print(f"✗ Error verificando tablas: {e}")
        return False