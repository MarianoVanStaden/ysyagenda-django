# 🗄️ Configuración de MariaDB para YSY Agenda

Esta guía te ayudará a configurar MariaDB para tu aplicación Django.

## 📋 Opciones de Despliegue con MariaDB

### 1. MariaDB Local (Desarrollo)

#### Instalación en Windows:

1. Descarga MariaDB desde [mariadb.org](https://mariadb.org/download/)
2. Instala MariaDB
3. Durante la instalación, configura una contraseña para root

#### Crear la base de datos:

```sql
-- Conectarse a MariaDB
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE ysyagenda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear un usuario específico para la aplicación
CREATE USER 'ysyagenda_user'@'localhost' IDENTIFIED BY 'tu_password_segura';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON ysyagenda.* TO 'ysyagenda_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

#### Configurar Django:

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key-generada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Opción 1: Usar DATABASE_URL (recomendado)
DATABASE_URL=mysql://ysyagenda_user:tu_password_segura@localhost:3306/ysyagenda

# Opción 2: Configuración manual (comenta DATABASE_URL si usas esta)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=ysyagenda
# DB_USER=ysyagenda_user
# DB_PASSWORD=tu_password_segura
# DB_HOST=localhost
# DB_PORT=3306

API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

#### Instalar el cliente de MySQL:

```powershell
# IMPORTANTE: En Windows necesitas Visual C++ 14.0 o superior
# Descarga "Microsoft C++ Build Tools" desde:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

pip install mysqlclient
```

**Si tienes problemas instalando mysqlclient en Windows**, usa alternativa:

```powershell
pip uninstall mysqlclient
pip install pymysql
```

Y agrega esto al principio de `ysyagenda/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

#### Migrar la base de datos:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

---

## 🌐 MariaDB en Producción

### Opción 1: Render con MariaDB Externo

Render no ofrece MariaDB directamente, pero puedes usar:

**1. FreeSQLDatabase.com (GRATIS hasta 250MB)**

1. Ve a [freesqldatabase.com](https://www.freesqldatabase.com)
2. Registra una cuenta gratuita
3. Crea una base de datos MySQL/MariaDB
4. Anota los datos de conexión:
   - Server
   - Username
   - Password
   - Database name
   - Port

**2. Configurar en Render:**

En las variables de entorno de Render:

```
DATABASE_URL=mysql://usuario:password@host:3306/database_name
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

### Opción 2: Railway con MariaDB

Railway no tiene MariaDB nativo, pero puedes usar MySQL que es compatible:

1. En tu proyecto de Railway, clic en **"+ New"**
2. Selecciona **"Database"** → **"MySQL"**
3. Railway creará automáticamente la variable `DATABASE_URL`

**Modificar el Build Command en Railway:**

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Opción 3: Hostinger (Hosting con cPanel - De pago)

Hostinger y muchos hostings tradicionales incluyen MariaDB:

1. En el panel de control (cPanel), ve a **"MySQL Databases"**
2. Crea una nueva base de datos
3. Crea un usuario y asígnalo a la base de datos
4. Anota los datos de conexión

**Variables de entorno (.env en el servidor):**

```env
DATABASE_URL=mysql://usuario:password@localhost:3306/database_name
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

### Opción 4: DigitalOcean App Platform + Managed Database

**1. Crear Managed Database:**

1. En DigitalOcean, ve a **"Databases"**
2. Clic en **"Create Database"**
3. Selecciona **"MySQL"** (compatible con MariaDB)
4. Elige el plan básico ($15/mes incluye DB y App)

**2. Obtener cadena de conexión:**

DigitalOcean te dará una cadena de conexión como:

```
mysql://doadmin:password@db-mysql-nyc1-12345-do-user-12345-0.db.ondigitalocean.com:25060/defaultdb?ssl-mode=REQUIRED
```

**3. Desplegar la App:**

- Conecta tu repositorio de GitHub
- Configura las variables de entorno con `DATABASE_URL`
- DigitalOcean manejará el resto

---

## 🔧 Migración de SQLite a MariaDB

Si ya tienes datos en SQLite y quieres migrarlos a MariaDB:

### Método 1: dumpdata/loaddata

```powershell
# 1. Exportar datos de SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data.json

# 2. Cambiar a MariaDB en settings.py o .env

# 3. Crear las tablas
python manage.py migrate

# 4. Importar los datos
python manage.py loaddata data.json
```

### Método 2: Django Database Router (para migración gradual)

Si necesitas mantener ambas bases de datos temporalmente.

---

## ⚡ Optimizaciones para MariaDB

### 1. Pooling de Conexiones

Instala django-db-connection-pool:

```powershell
pip install django-db-connection-pool
```

En `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
        },
        # ... resto de configuración
    }
}
```

### 2. Índices para mejor rendimiento

En tus modelos, agrega índices:

```python
class MiModelo(models.Model):
    campo = models.CharField(max_length=100, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['campo1', 'campo2']),
        ]
```

---

## 🔍 Solución de Problemas

### Error: "django.db.utils.OperationalError: (2002, "Can't connect to MySQL server")"

**Solución:**
- Verifica que MariaDB está corriendo: `mysql --version`
- Verifica las credenciales en tu `.env`
- Verifica que el host y puerto son correctos

### Error: "mysqlclient installation failed"

**Solución en Windows:**
```powershell
# Usa pymysql en su lugar
pip install pymysql
```

En `ysyagenda/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Error: "Unknown column in 'field list'"

**Solución:**
```powershell
# Asegúrate de correr las migraciones
python manage.py migrate
python manage.py migrate --run-syncdb
```

### Lentitud en las consultas

**Solución:**
1. Habilita el query logging:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

2. Analiza y optimiza consultas lentas
3. Agrega índices donde sea necesario

---

## 📊 Backup de la Base de Datos

### Backup Manual:

```bash
# Backup
mysqldump -u usuario -p ysyagenda > backup_$(date +%Y%m%d).sql

# Restaurar
mysql -u usuario -p ysyagenda < backup_20250101.sql
```

### Backup Automático con Python:

```python
import subprocess
import datetime

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.sql"
    subprocess.run([
        'mysqldump',
        '-u', 'usuario',
        '-p', 'password',
        'ysyagenda',
        '--result-file', filename
    ])
```

---

## ✅ Checklist de Producción con MariaDB

- [ ] MariaDB instalado y configurado
- [ ] Base de datos creada con charset utf8mb4
- [ ] Usuario específico creado (no usar root en producción)
- [ ] `DATABASE_URL` configurada en variables de entorno
- [ ] `mysqlclient` o `pymysql` instalado
- [ ] Migraciones aplicadas: `python manage.py migrate`
- [ ] Conexión SSL habilitada (en producción)
- [ ] Backups automáticos configurados
- [ ] Monitoreo de la base de datos activo

---

## 🔗 Recursos Adicionales

- [MariaDB Documentation](https://mariadb.org/documentation/)
- [Django MySQL Notes](https://docs.djangoproject.com/en/5.2/ref/databases/#mysql-notes)
- [mysqlclient GitHub](https://github.com/PyMySQL/mysqlclient)
- [Free MySQL Hosting Options](https://www.freesqldatabase.com/)

---

**¡Importante!** No olvides agregar `.env` a tu `.gitignore` para no exponer las credenciales de tu base de datos.
