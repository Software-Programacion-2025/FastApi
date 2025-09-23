# 📚 Documentación ToDo System API

## 🎯 Guías de Usuario

### 🚀 Para Empezar Rápidamente

**[Guía de Swagger UI](./SWAGGER_GUIDE.md)** - Documentación interactiva (Recomendado)

- ✅ No requiere instalaciones adicionales
- ✅ Prueba la API directamente en el navegador
- ✅ Perfecto para desarrollo y testing de tareas

### 📮 Para Desarrollo Avanzado

**[Guía de Postman](./POSTMAN_GUIDE.md)** - Cliente API profesional

- ✅ Automatización de tests
- ✅ Collections reutilizables para usuarios y tareas
- ✅ Scripts y variables de entorno
- ✅ Ideal para integración y testing automático

## 📖 Documentación Técnica

### 🏠 General

**[README.md](./README.md)** - Documentación principal del proyecto

- Instalación y configuración
- Arquitectura del sistema
- Usuarios de prueba
- Variables de entorno

### 📋 Referencia

**[API Reference](./API_REFERENCE.md)** - Especificación completa de endpoints

- Todos los endpoints disponibles
- Ejemplos de request/response
- Códigos de error
- Parámetros detallados

### 🔒 Seguridad

**[Security Guide](./SECURITY_GUIDE.md)** - Guía técnica de autenticación

- JWT implementation
- Sistema de permisos
- Middleware de autenticación
- Buenas prácticas de seguridad

## 🚀 Quick Start

### Opción 1: Swagger UI (Principiantes)

```bash
# 1. Iniciar servidor
uvicorn app:app --reload

# 2. Abrir navegador
http://localhost:5000/docs

# 3. Login: admin / admin123
# 4. Autorizar con el token
# 5. ¡Explorar todos los endpoints!
```

### Opción 2: Postman (Avanzado)

```bash
# 1. Iniciar servidor
uvicorn app:app --reload

# 2. Seguir POSTMAN_GUIDE.md para:
#    - Configurar environment
#    - Crear collection  
#    - Automatizar autenticación
```

## 🔑 Credenciales de Prueba

| Usuario    | Contraseña | Rol           | Uso Recomendado               |
| ---------- | ----------- | ------------- | ----------------------------- |
| admin      | admin123    | Administrador | Probar todas las funciones    |
| gerente01  | gerente123  | Gerente       | Testing de permisos medios    |
| empleado01 | empleado123 | Empleado      | Testing de permisos limitados |

## 📊 Flujo de Trabajo Recomendado

### 1. 🎓 Aprendizaje (Primera Vez)

```
README.md → SWAGGER_GUIDE.md → Swagger UI
```

### 2. 🧪 Testing y Desarrollo

```
POSTMAN_GUIDE.md → Collection Setup → API_REFERENCE.md
```

### 3. 🔧 Implementación y Seguridad

```
SECURITY_GUIDE.md → JWT Implementation → Production Setup
```

## 🆘 Resolución de Problemas

### Error 401 (Unauthorized)

- ✅ Verificar token en Authorization
- ✅ Token no expirado (30 min)
- ✅ Formato: `Bearer token_aqui`

### Error 403 (Forbidden)

- ✅ Usuario con permisos suficientes
- ✅ Usar admin para testing completo
- ✅ Verificar permisos en base de datos

### Servidor no responde

- ✅ Servidor corriendo en puerto 5000
- ✅ Base de datos creada (seeders ejecutados)
- ✅ Variables de entorno configuradas

## 🔄 Flujo de Autenticación

```
1. POST /usuarios/login          → Obtener token
2. Configurar Authorization      → Bearer <token>
3. Usar endpoints protegidos     → API completa disponible
4. Token expira (30 min)         → Repetir paso 1
```

## 🛠️ Stack Tecnológico

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **JWT** - Autenticación
- **bcrypt** - Hash de contraseñas
- **SQLite** - Base de datos
- **Swagger/OpenAPI** - Documentación automática

## 📞 Soporte

Para dudas específicas:

1. **Instalación/Config**: [`README.md`](./README.md)
2. **Uso Swagger**: [`SWAGGER_GUIDE.md`](./SWAGGER_GUIDE.md)
3. **Uso Postman**: [`POSTMAN_GUIDE.md`](./POSTMAN_GUIDE.md)
4. **Endpoints**: [`API_REFERENCE.md`](./API_REFERENCE.md)
5. **Seguridad**: [`SECURITY_GUIDE.md`](./SECURITY_GUIDE.md)

---

**🚀 ¡Elige tu herramienta favorita y comienza a usar la API!**
