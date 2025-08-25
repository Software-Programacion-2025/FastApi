# Documentación Técnica: Validaciones en Servicios

> **📚 Documentación Principal**: Ver [README.md](./README.md) para información general del proyecto.

Este documento proporciona detalles técnicos específicos sobre las validaciones y el manejo de errores implementado en la capa de servicios de la aplicación.

## Resumen Ejecutivo

Los servicios implementan un sistema completo de validaciones con:
- ✅ Logging estructurado para monitoreo
- ✅ Gestión segura de transacciones
- ✅ Validaciones exhaustivas de entrada
- ✅ Manejo robusto de errores de base de datos
- ✅ Funciones de utilidad para validaciones comunes

### 1. Importaciones y Configuración

#### Nuevas Importaciones
- `SQLAlchemyError`, `IntegrityError`: Para manejo específico de errores de base de datos
- `logging`: Para registro detallado de operaciones y errores
- `re`: Para validaciones con expresiones regulares

#### Configuración de Logging
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### 2. Servicios de Tareas (`tasks/services.py`)

#### Funciones Implementadas con Validaciones

##### `get_all_tasks()`
- **Manejo de errores**: SQLAlchemyError, Exception general
- **Logging**: Registro del número de tareas obtenidas
- **Limpieza**: Cierre automático de sesión en bloque finally

##### `create_task(task_data: TaskCreate)`
- **Validaciones**:
  - Usuario existe y está activo
  - Título no vacío (strip)
  - Descripción opcional limpia
- **Transacciones**: Uso de `flush()` antes de confirmar
- **Rollback**: Automático en caso de error
- **Logging**: Registro de creación exitosa con detalles

##### `update_task_state(task_id: int, state_data: TaskUpdateState)`
- **Validaciones**:
  - ID de tarea válido (> 0)
  - Tarea existe
- **Logging**: Registro de cambios de estado
- **Manejo de atributos**: Uso de `getattr/setattr` para compatibilidad

##### `get_task_by_id(task_id: int)`
- **Validaciones**: ID de tarea válido
- **Eager loading**: Carga de usuarios relacionados
- **Logging**: Registro de búsquedas exitosas y fallidas

##### `assign_user_to_task(task_id: int, assign_data: TaskAssignUser)`
- **Validaciones**:
  - ID de tarea válido
  - ID de usuario requerido y no vacío
  - Tarea existe
  - Usuario existe y está activo
  - Usuario no está ya asignado
- **Logging**: Registro de asignaciones exitosas

##### `unassign_user_from_task(task_id: int, user_id: str)`
- **Validaciones**:
  - ID de tarea válido
  - ID de usuario requerido
  - Tarea existe
  - Usuario existe (puede estar inactivo)
  - Usuario está asignado a la tarea
- **Logging**: Registro de desasignaciones exitosas

### 3. Servicios de Usuarios (`users/services.py`)

#### Funciones de Utilidad

##### `validate_email_format(email: str) -> bool`
- Validación de formato de email usando regex
- Patrón: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

#### Funciones Implementadas con Validaciones

##### `getAllUsers()`
- **Filtrado**: Solo usuarios activos (delete_at == None)
- **Logging**: Registro del número de usuarios obtenidos
- **Manejo de errores**: SQLAlchemyError, Exception general

##### `getAllUsersDeleted()`
- **Filtrado**: Solo usuarios eliminados (delete_at != None)
- **Logging**: Registro del número de usuarios eliminados
- **Manejo de errores**: SQLAlchemyError, Exception general

##### `getOneUser(id: str)`
- **Validaciones**: ID requerido y no vacío
- **Filtrado**: Solo usuarios activos
- **Logging**: Registro de búsquedas exitosas y fallidas

##### `postUser(user: UserInsert)`
- **Validaciones**:
  - Datos de usuario requeridos
  - Nombre y apellido requeridos y no vacíos
  - Email requerido y formato válido
  - Contraseña mínimo 6 caracteres
  - Edad entre 1 y 150 años
  - Email único en la base de datos
- **Normalización**:
  - Trim de espacios en strings
  - Email en minúsculas
- **Logging**: Registro de creación exitosa con detalles

##### `putUser(id: str, user: UserUpdate)`
- **Validaciones**:
  - ID requerido y no vacío
  - Datos de usuario requeridos
  - Validaciones específicas por campo
  - Email único (excluye el usuario actual)
- **Tracking**: Registro de valores anteriores
- **Logging**: Registro de cambios realizados

##### `deleteUser(id: str)`
- **Validaciones**: ID requerido y no vacío
- **Soft Delete**: Uso de campo delete_at
- **Filtrado**: Solo usuarios activos
- **Logging**: Registro de eliminación exitosa

##### `recoveryUser(id: str)`
- **Validaciones**: ID requerido y no vacío
- **Filtrado**: Solo usuarios eliminados
- **Actualización**: Campo update_at actualizado
- **Logging**: Registro de recuperación exitosa

### 4. Manejo de Excepciones por Tipo

#### Jerarquía de Manejo
1. **ValueError**: Errores de validación de entrada y lógica de negocio
2. **IntegrityError**: Errores de integridad de base de datos (emails duplicados)
3. **SQLAlchemyError**: Errores generales de base de datos
4. **Exception**: Errores inesperados

#### Estrategias de Rollback
- **Automático**: En todos los casos de error que implican transacciones
- **Condicional**: Solo si la sesión de base de datos existe
- **Logging**: Registro detallado del tipo de error y contexto

### 5. Características de Logging

#### Niveles de Log
- **INFO**: Operaciones exitosas, estadísticas
- **WARNING**: Intentos de operaciones inválidas
- **ERROR**: Errores de base de datos y excepciones

#### Información Registrada
- **Operaciones exitosas**: Detalles de la operación y resultados
- **Búsquedas fallidas**: IDs no encontrados
- **Errores de validación**: Intentos de operaciones inválidas
- **Errores de sistema**: Detalles técnicos para debugging

### 6. Gestión de Recursos

#### Sesiones de Base de Datos
- **Finally blocks**: Cierre garantizado de sesiones
- **Verificación de existencia**: Antes de cerrar sesiones
- **Rollback automático**: En casos de error

#### Transacciones
- **Commit explícito**: Solo después de validaciones exitosas
- **Flush estratégico**: Para obtener IDs antes del commit final
- **Refresh**: Para obtener datos actualizados después del commit

### 7. Beneficios de las Mejoras

1. **Robustez**: Manejo completo de casos de error
2. **Observabilidad**: Logging detallado para monitoreo y debugging
3. **Integridad**: Validaciones exhaustivas de datos
4. **Rendimiento**: Gestión eficiente de recursos de base de datos
5. **Mantenibilidad**: Código más estructurado y documentado
6. **Seguridad**: Validación de entradas y prevención de inyecciones
7. **Consistencia**: Manejo uniforme de errores en todos los servicios

### 8. Ejemplos de Logging

#### Operación Exitosa
```
INFO: Usuario creado exitosamente: 123e4567-e89b-12d3-a456-426614174000 - john.doe@example.com
```

#### Validación Fallida
```
WARNING: Intento de crear usuario con email duplicado: john.doe@example.com
```

#### Error de Sistema
```
ERROR: Error de base de datos al crear usuario: connection timeout
```

Este sistema de validaciones y manejo de errores en los servicios proporciona una capa robusta y confiable para todas las operaciones de la aplicación.
