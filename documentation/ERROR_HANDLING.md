# Documentación Técnica: Manejo de Errores HTTP

> **📚 Documentación Principal**: Ver [README.md](./README.md) para información general del proyecto.

Este documento proporciona detalles técnicos específicos sobre el sistema de validaciones y manejo de errores HTTP implementado en todas las rutas de la API.

## Resumen Ejecutivo

El proyecto implementa un sistema robusto de manejo de errores HTTP con:
- ✅ Códigos de estado HTTP estandarizados
- ✅ Validaciones exhaustivas en rutas
- ✅ Mensajes de error descriptivos
- ✅ Jerarquía de manejo de excepciones
- ✅ Funciones de utilidad para validaciones comunes

### 1. Importaciones Actualizadas
- Se agregó `status` de FastAPI para usar códigos de estado HTTP consistentes
- Se importó `SQLAlchemyError` e `IntegrityError` para manejo específico de errores de base de datos
- Se agregó `re` para validaciones de expresiones regulares

### 2. Códigos de Estado HTTP Estandarizados
- `HTTP_200_OK` (200): Operaciones exitosas
- `HTTP_201_CREATED` (201): Recursos creados exitosamente
- `HTTP_400_BAD_REQUEST` (400): Errores de validación de entrada
- `HTTP_404_NOT_FOUND` (404): Recursos no encontrados
- `HTTP_409_CONFLICT` (409): Conflictos de integridad (ej: email duplicado)
- `HTTP_500_INTERNAL_SERVER_ERROR` (500): Errores internos del servidor

### 3. Validaciones Implementadas

#### Rutas de Tareas (`tasks/routes.py`)
- **ID de tarea**: Validación de números positivos
- **Título de tarea**: Validación de campo requerido y no vacío
- **Estados válidos**: Validación contra lista de estados permitidos (`pending`, `in_progress`, `completed`, `cancelled`)
- **ID de usuario**: Validación de campo requerido y no vacío

#### Rutas de Usuarios (`users/ruotes.py`)
- **UUID**: Validación de formato de ID de usuario
- **Email**: Validación de formato usando expresión regular
- **Campos requeridos**: Validación de firstName, lastName, emails
- **Edad**: Validación de rango (1-150 años)
- **Contraseña**: Validación de longitud mínima (6 caracteres)

#### Rutas por Defecto (`default/routes.py`)
- **Archivo favicon**: Validación de existencia de archivo
- **Health check**: Endpoint adicional para monitoreo

### 4. Manejo de Excepciones

#### Jerarquía de Manejo de Errores
1. **HTTPException**: Se re-lanza para mantener el código de estado original
2. **ValueError**: Errores de lógica de negocio (404 o 400 según contexto)
3. **IntegrityError**: Errores de integridad de base de datos (409)
4. **SQLAlchemyError**: Errores generales de base de datos (500)
5. **Exception**: Errores inesperados (500)

#### Mensajes de Error Descriptivos
- Mensajes claros y específicos para cada tipo de error
- Información contextual (ej: ID del recurso no encontrado)
- Sugerencias cuando es apropiado (ej: estados válidos)

### 5. Funciones de Utilidad

#### `validate_email(email: str) -> bool`
Valida el formato de email usando expresión regular.

#### `validate_uuid(uuid_string: str) -> bool`
Valida que una cadena tenga formato UUID válido.

### 6. Documentación Mejorada
- Docstrings agregados a todas las funciones de ruta
- Descripción clara del propósito de cada endpoint
- Comentarios explicativos en el código

## Beneficios de las Mejoras

1. **Mejor Experiencia de Usuario**: Mensajes de error claros y específicos
2. **Seguridad Mejorada**: Validación exhaustiva de entradas
3. **Mantenibilidad**: Código más estructurado y documentado
4. **Debugging Simplificado**: Logs más informativos y errores categorizados
5. **Estándares HTTP**: Uso correcto de códigos de estado HTTP
6. **Robustez**: Manejo de casos edge y errores inesperados

## Ejemplos de Respuestas de Error

### Error 400 - Bad Request
```json
{
  "detail": "El título de la tarea es requerido"
}
```

### Error 404 - Not Found
```json
{
  "detail": "Usuario con ID 123e4567-e89b-12d3-a456-426614174000 no encontrado"
}
```

### Error 409 - Conflict
```json
{
  "detail": "Email ya está registrado"
}
```

### Error 500 - Internal Server Error
```json
{
  "detail": "Error interno del servidor al crear el usuario"
}
```

## Endpoints Adicionales

### Health Check
- **GET** `/health`: Endpoint para monitoreo de salud del servicio
- Retorna información sobre el estado del servicio y timestamp

Este sistema de validaciones y manejo de errores proporciona una API robusta, segura y fácil de usar.
