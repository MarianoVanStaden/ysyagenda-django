# 🚀 GUÍA RÁPIDA DE DESPLIEGUE

## ✅ Archivos Creados para Producción

1. **`.env.example`** - Plantilla de variables de entorno
2. **`DEPLOYMENT.md`** - Guía completa de despliegue
3. **`MARIADB_SETUP.md`** - Guía específica para MariaDB
4. **`Procfile`** - Configuración para servicios de hosting
5. **`runtime.txt`** - Versión de Python
6. **`requirements.txt`** - Actualizado con dependencias de producción

## 🎯 Pasos Rápidos para Subir a Internet

### 1️⃣ Instalar Dependencias

```powershell
pip install PyMySQL cryptography python-dotenv whitenoise dj-database-url
```

### 2️⃣ Generar SECRET_KEY

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3️⃣ Elegir una Plataforma de Hosting

#### 🌟 OPCIÓN A: Render (GRATIS - Recomendado)

1. **Crear cuenta**: [render.com](https://render.com)
2. **Subir código a GitHub**:
   ```powershell
   git add .
   git commit -m "Preparado para producción"
   git push
   ```
3. **En Render**:
   - New → Web Service
   - Conectar repositorio GitHub
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```
     gunicorn ysyagenda.wsgi:application
     ```
4. **Variables de entorno en Render**:
   ```
   SECRET_KEY=tu-secret-key-generada
   DEBUG=False
   ALLOWED_HOSTS=tu-app.onrender.com
   DATABASE_URL=mysql://user:pass@host:3306/dbname
   API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
   ```

#### 🚂 OPCIÓN B: Railway (GRATIS $5 crédito/mes)

1. **Crear cuenta**: [railway.app](https://railway.app)
2. **Subir código a GitHub** (igual que arriba)
3. **En Railway**:
   - New Project → Deploy from GitHub
   - Seleccionar repositorio
   - Agregar MySQL: New → Database → MySQL
4. **Variables de entorno** (igual que Render)

#### 🐍 OPCIÓN C: PythonAnywhere (GRATIS - Limitado)

1. **Crear cuenta**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Subir código** y seguir pasos en `DEPLOYMENT.md` sección PythonAnywhere

### 4️⃣ Configurar Base de Datos MariaDB

#### Para desarrollo local:
Ver guía completa en `MARIADB_SETUP.md`

#### Para producción:
- **FreeSQLDatabase**: [freesqldatabase.com](https://www.freesqldatabase.com) - GRATIS 250MB
- **Railway MySQL**: Se crea automáticamente al agregar MySQL
- **Render**: Necesitas DB externa (usa FreeSQLDatabase)

### 5️⃣ Verificar Despliegue

1. Accede a tu URL: `https://tu-app.onrender.com`
2. Prueba todas las páginas:
   - `/` - Home
   - `/turnos/` - Turnos
   - `/especialidades/` - Especialidades
   - `/profesionales/` - Profesionales

## 📝 Comandos Útiles

```powershell
# Generar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Probar con gunicorn localmente
gunicorn ysyagenda.wsgi:application
```

## 🗄️ DATABASE_URL Formato

```
# SQLite (desarrollo)
sqlite:///./db.sqlite3

# MariaDB/MySQL
mysql://usuario:password@host:3306/nombre_base_datos

# PostgreSQL
postgresql://usuario:password@host:5432/nombre_base_datos
```

## 🔐 Archivo .env (Crear en producción)

```env
SECRET_KEY=tu-secret-key-muy-segura-generada
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=mysql://user:pass@host:3306/dbname
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

## ⚠️ IMPORTANTE - Antes de Desplegar

- [ ] Generar nueva SECRET_KEY (NO usar la del código)
- [ ] Verificar que DEBUG=False en producción
- [ ] Configurar ALLOWED_HOSTS correctamente
- [ ] Tener base de datos MariaDB lista
- [ ] Probar localmente con gunicorn
- [ ] Hacer backup de tu código

## 🆘 Problemas Comunes

### "No module named 'pymysql'"
```powershell
pip install PyMySQL cryptography
```

### "Cannot connect to database"
- Verifica DATABASE_URL en variables de entorno
- Verifica que la base de datos existe
- Verifica usuario y contraseña

### "Static files not found"
```powershell
python manage.py collectstatic --noinput
```

### Aplicación muy lenta en Render (plan gratuito)
- Normal en plan gratuito: se "duerme" después de 15 min sin uso
- Primera carga puede tardar 30-60 segundos
- Considera Railway o plan de pago

## 📚 Documentación Completa

- **DEPLOYMENT.md** - Guía detallada de todas las opciones de hosting
- **MARIADB_SETUP.md** - Configuración completa de MariaDB
- **README.md** - Documentación del proyecto

## 🎉 ¡Listo!

Una vez configurado, tu aplicación estará disponible 24/7 en internet.

**Próximos pasos**:
1. Compartir URL con usuarios
2. Monitorear logs regularmente
3. Configurar dominio personalizado (opcional)
4. Hacer backups periódicos de la base de datos

---

**¿Necesitas ayuda?** Revisa las guías completas en los archivos .md
