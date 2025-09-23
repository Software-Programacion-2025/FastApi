# Seeders - Sistema Kick Shopping

Este directorio contiene todos los seeders organizados para la carga inicial de datos del sistema de tienda de calzado deportivo.

## 📋 Descripción

Los seeders están divididos por funcionalidad para facilitar el mantenimiento y permitir la ejecución individual o completa según las necesidades del sistema Kick Shopping.

## 📁 Estructura de Archivos

```
seeders/
├── README.md                 # Esta documentación
├── seed_main.py             # Seeder principal (ejecuta todos)
├── seed_roles.py            # Carga de roles del sistema
├── seed_usuarios.py         # Carga de usuarios de ejemplo
├── seed_permisos.py         # Carga de permisos del sistema
└── seed_rol_permisos.py     # Asignación de permisos a roles
```

## 🚀 Uso Rápido

### Seeding Completo (Recomendado)

```bash
cd seeders/
python seed_main.py all
```

### Seeding Individual

```bash
# Solo roles
python seed_main.py roles

# Solo usuarios
python seed_main.py usuarios

# Solo permisos
python seed_main.py permisos

# Solo asignaciones rol-permiso
python seed_main.py rol-permisos
```

### Ayuda

```bash
python seed_main.py help
```

## 📊 Secuencia de Ejecución

**⚠️ IMPORTANTE:** Debe respetarse el siguiente orden para mantener la integridad referencial:

### 1. Roles (`seed_roles.py`)

- **Depende de:** Nada
- **Carga:** Roles básicos del sistema
- **Datos:**
  - Administrador (acceso completo)
  - Gerente (gestión operativa)
  - Empleado (operaciones básicas)
  - Cliente (usuario final de la tienda)

### 2. Usuarios (`seed_usuarios.py`)

- **Depende de:** Roles
- **Carga:** Usuarios de ejemplo para cada rol
- **Datos:**
  - admin / admin123 (Administrador)
  - gerente01 / gerente123 (Gerente)
  - empleado01 / empleado123 (Empleado)
  - cliente01 / cliente123 (Cliente)

### 3. Permisos (`seed_permisos.py`)

- **Depende de:** Nada
- **Carga:** Todos los permisos detallados del sistema
- **Módulos:** usuarios, roles, productos, cart_items, permisos

### 4. Asignaciones Rol-Permiso (`seed_rol_permisos.py`)

- **Depende de:** Roles y Permisos
- **Carga:** Matriz de permisos por rol
- **Lógica:**
  - **Administrador:** Todos los permisos
  - **Gerente:** Gestión completa excepto administración de usuarios/roles
  - **Empleado:** Solo lectura y operaciones básicas de productos
  - **Cliente:** Solo lectura de productos y gestión de carrito

## 🔧 Ejecución Individual de Seeders

Si necesitas ejecutar seeders individuales, puedes hacerlo directamente:

```bash
# Roles
cd seeders/
python seed_roles.py

# Usuarios
python seed_usuarios.py

# Permisos
python seed_permisos.py

# Asignaciones
python seed_rol_permisos.py
```

## 📋 Datos Cargados

### Roles

| Rol           | Descripción                                    | Permisos Base      |
| ------------- | ---------------------------------------------- | ------------------ |
| Administrador | Acceso completo al sistema                     | all                |
| Gerente       | Gestión de productos, usuarios y operaciones  | manage             |
| Empleado      | Operaciones básicas de productos y consulta   | read,create        |
| Cliente       | Visualización de productos y gestión de carrito| read (limitado)    |

### Usuarios de Ejemplo

| Usuario    | Contraseña  | Rol           | Nombre Completo              |
| ---------- | ----------- | ------------- | ---------------------------- |
| admin      | admin123*   | Administrador | Administrador del Sistema    |
| gerente01  | gerente123* | Gerente       | María González Gerente       |
| empleado01 | empleado123*| Empleado      | Juan Pérez Empleado          |
| cliente01  | cliente123* | Cliente       | Ana López Cliente            |

**\* Las contraseñas se almacenan encriptadas usando bcrypt para mayor seguridad**

### Permisos por Módulo

#### 👥 Usuarios

- usuarios.listar, usuarios.crear, usuarios.ver, usuarios.actualizar, usuarios.eliminar

#### 📋 Roles

- roles.listar, roles.crear, roles.ver, roles.actualizar, roles.eliminar

#### 👟 Productos

- productos.listar, productos.crear, productos.ver, productos.actualizar, productos.eliminar

#### 🛒 Cart Items (Carrito de Compras)

- cart_items.listar, cart_items.crear, cart_items.ver, cart_items.actualizar, cart_items.eliminar

#### 🔐 Permisos (Meta-permisos)

- permisos.listar, permisos.crear, permisos.actualizar, permisos.eliminar, permisos.asignar

## ⚡ Características de los Seeders

### 🛡️ Seguridad

- Verificación de existencia antes de crear duplicados
- Transacciones con rollback en caso de error
- Validación de integridad referencial

### 🔄 Idempotencia

- Los seeders pueden ejecutarse múltiples veces sin crear duplicados
- Verificación automática de datos existentes

### 📝 Logging

- Registro detallado de todas las operaciones
- Diferenciación entre creación y omisión de datos existentes

### 🎯 Flexibilidad

- Ejecución individual o completa
- Parámetros por línea de comandos
- Configuración centralizada de datos

## 🚨 Troubleshooting

### Error: "Rol no encontrado"

- **Causa:** Intentar cargar usuarios sin haber cargado roles primero
- **Solución:** Ejecutar `seed_roles.py` antes que `seed_usuarios.py`

### Error: "Permiso no encontrado"

- **Causa:** Intentar asignar permisos sin haberlos cargado
- **Solución:** Ejecutar `seed_permisos.py` antes que `seed_rol_permisos.py`

### Error: "Tabla no existe"

- **Causa:** Las tablas no fueron creadas
- **Solución:** Los seeders crean automáticamente las tablas, verificar permisos de escritura en la BD

### Datos duplicados

- **Causa:** Normal, los seeders verifican existencia
- **Solución:** Los mensajes "ya existe" son normales y seguros

## 📝 Notas Adicionales

1. **Contraseñas encriptadas:** Las contraseñas se encriptan automáticamente usando bcrypt antes de ser guardadas
2. **Contraseñas por defecto:** Todas las contraseñas son de ejemplo y deben cambiarse en producción
3. **Roles personalizados:** Puedes agregar nuevos roles editando `seed_roles.py`
4. **Permisos adicionales:** Nuevos permisos se agregan en `seed_permisos.py`
5. **Configuración de permisos:** La matriz rol-permiso se configura en `seed_rol_permisos.py`
6. **Seguridad:** El seeder usa la misma función de encriptación que el sistema de autenticación (`hash_password`)

## 🔗 Enlaces Relacionados

- [Documentación de Roles](../roles/)
- [Documentación de Usuarios](../usuarios/)
- [Documentación de Permisos](../permisos/)
- [Documentación de Productos](../productos/)
- [Middleware de Autenticación](../middlewares/auth.py)

---

**💡 Tip:** Siempre ejecuta `seed_main.py all` para un seeding completo y consistente del sistema Kick Shopping.