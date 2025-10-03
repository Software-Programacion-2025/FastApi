"""
Seeder para asignar roles a usuarios existentes
"""
import sqlite3
import os

def assign_roles_to_users():
    """Asignar roles a usuarios existentes usando SQL directo"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mybase.db')
    
    print("=== Iniciando asignación de roles a usuarios ===")
    print(f"Usando base de datos: {db_path}")
    
    # Mapeo de emails a roles
    user_role_mapping = {
        "admin@sistema.com": "Administrador",
        "maria.gonzalez@empresa.com": "Gerente", 
        "juan.perez@empresa.com": "Empleado",
        "ana.lopez@empresa.com": "Cajero"
    }
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        assignments_made = 0
        
        for email, rol_nombre in user_role_mapping.items():
            # Buscar usuario
            cursor.execute("SELECT id FROM users WHERE emails = ?", (email,))
            user_result = cursor.fetchone()
            if not user_result:
                print(f"⚠️  Usuario {email} no encontrado, omitiendo...")
                continue
            user_id = user_result[0]
                
            # Buscar rol
            cursor.execute("SELECT rol_id FROM roles WHERE rol_nombre = ?", (rol_nombre,))
            rol_result = cursor.fetchone()
            if not rol_result:
                print(f"⚠️  Rol {rol_nombre} no encontrado, omitiendo...")
                continue
            rol_id = rol_result[0]
                
            # Verificar si ya tiene el rol asignado
            cursor.execute("""
                SELECT COUNT(*) FROM user_rol_association 
                WHERE user_id = ? AND rol_id = ?
            """, (user_id, rol_id))
            
            if cursor.fetchone()[0] > 0:
                print(f"- Usuario {email} ya tiene el rol {rol_nombre}, omitiendo...")
                continue
                
            # Asignar rol al usuario
            cursor.execute("""
                INSERT INTO user_rol_association (user_id, rol_id, assigned_at) 
                VALUES (?, ?, datetime('now'))
            """, (user_id, rol_id))
            
            assignments_made += 1
            print(f"✓ Asignando rol '{rol_nombre}' al usuario '{email}'")
        
        conn.commit()
        
        if assignments_made > 0:
            print(f"✅ Se realizaron {assignments_made} asignaciones de roles exitosamente")
        else:
            print("ℹ️ Todas las asignaciones ya existían")
            
        # Mostrar estado final
        print("\n=== Estado de asignaciones ===")
        cursor.execute("""
            SELECT u.emails, r.rol_nombre 
            FROM users u 
            JOIN user_rol_association ura ON u.id = ura.user_id
            JOIN roles r ON ura.rol_id = r.rol_id
            ORDER BY u.emails, r.rol_nombre
        """)
        
        results = cursor.fetchall()
        if results:
            print("Roles asignados:")
            for email, rol in results:
                print(f"  - {email}: {rol}")
        else:
            print("No hay roles asignados")
            
    except Exception as e:
        print(f"✗ Error al asignar roles: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Seeder de Asignación de Roles ===")
    assign_roles_to_users()
    print("=== Finalizado ===")