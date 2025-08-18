# 🚀 FastApi

**Proyecto de Ejemplo con FastApi**

---

---

## 📁 Estructura General del Proyecto

```text
alembic.ini
app.py
mibase.db
README.md
requirements.txt
alembic/
	env.py
	versions/
config/
	basemodel.py
	cnx.py
default/
	routes.py
middlewares/
	auth.py
tasks/
	model.py
	routes.py
	services.py
users/
	model.py
	services.py
```

---

---

## ⚡ Uso de Uvicorn

Para iniciar el servidor de desarrollo ejecuta:

```bash
uvicorn app:app --reload
```

Esto levantará el servidor en modo desarrollo y recargará automáticamente ante cambios en el código.

---

---

## 🗂️ Agregado y Uso de Alembic

Alembic se utiliza para gestionar las migraciones de la base de datos.

### 🛠️ Instalación

Instala Alembic usando pip:

```bash
pip install alembic

alembic init alembic
```

[Documentacion Alembic](https://alembic.sqlalchemy.org/en/latest/front.html#installation "Docu")

### ⚙️ Configuración previa antes de la primera migración

1. **Configura la URL de la base de datos** en el archivo `alembic.ini`:

   - Por ejemplo, para SQLite:

     ```ini
     sqlalchemy.url = sqlite:///mibase.db
     ```
2. **Importa y registra tus modelos** en `alembic/env.py`:

   - Asegúrate de importar todos los modelos y asignar `target_metadata` a la metadata base de tus modelos:

     ```python
     from config.basemodel import Base
     from users import model as users_model
     from tasks import model as tasks_model
     target_metadata = Base.metadata
     ```

### 📝 Comandos principales

- Generar una nueva migración automáticamente:

  ```bash
  alembic revision --autogenerate -m "mensaje de la migración"
  ```
- Aplicar las migraciones pendientes:

  ```bash
  alembic upgrade head
  ```

---

## 🌱 Uso de Seeders

Para poblar la base de datos con datos de ejemplo puedes usar el seeder incluido en el archivo `seed.py`.

### Instalación de dependencias

Asegúrate de tener instalados:

- Typer
- Faker

Puedes instalarlos con:

```bash
pip install typer faker
```

### Uso del Seeder

Ejecuta el siguiente comando para crear 10 usuarios de ejemplo:

```bash
python seed.py
```

Puedes cambiar la cantidad de usuarios agregando el parámetro `--count`:

```bash
python seed.py --count 20
```

Esto es útil para pruebas y desarrollo, y puedes modificar el seeder para poblar otras tablas según tus necesidades.

---
