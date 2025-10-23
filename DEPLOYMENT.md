# 🚀 Guía de Despliegue - YSY Agenda

Esta guía te ayudará a desplegar tu aplicación Django en internet. Tienes varias opciones según tus necesidades.

## 📋 Tabla de Contenidos
1. [Preparación Inicial](#preparación-inicial)
2. [Opciones de Hosting](#opciones-de-hosting)
3. [Despliegue en Render (Recomendado - GRATIS)](#despliegue-en-render)
4. [Despliegue en Railway](#despliegue-en-railway)
5. [Despliegue en PythonAnywhere](#despliegue-en-pythonanywhere)
6. [Post-Despliegue](#post-despliegue)

---

## 🔧 Preparación Inicial

### 1. Instalar las nuevas dependencias

```powershell
pip install -r requirements.txt
```

### 2. Generar una nueva SECRET_KEY para producción

Ejecuta en Python:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Guarda este valor, lo necesitarás más adelante.

### 3. Recolectar archivos estáticos

```powershell
python manage.py collectstatic --noinput
```

### 4. Verificar que todo funciona localmente

```powershell
# Crear las variables de entorno temporalmente
$env:DEBUG="False"
$env:SECRET_KEY="tu-secret-key-generada"
$env:ALLOWED_HOSTS="localhost,127.0.0.1"

# Ejecutar con gunicorn
gunicorn ysyagenda.wsgi:application
```

Accede a `http://localhost:8000` y verifica que todo funcione.

---

## 🌐 Opciones de Hosting

| Plataforma | Precio | Pros | Contras |
|------------|--------|------|---------|
| **Render** | GRATIS (Plan básico) | Fácil, PostgreSQL incluido, SSL automático | Duerme si no hay tráfico |
| **Railway** | GRATIS ($5 crédito/mes) | Muy fácil, rápido | Créditos limitados |
| **PythonAnywhere** | GRATIS (limitado) | Especializado en Python | Configuración manual |
| **Heroku** | De pago | Muy conocido | Ya no tiene plan gratuito |
| **DigitalOcean** | Desde $4/mes | Control total | Requiere más conocimientos |

**Recomendación**: Render es la mejor opción gratuita actualmente.

---

## 🎯 Despliegue en Render (GRATIS)

### Paso 1: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub

### Paso 2: Subir el código a GitHub

```powershell
# Si aún no has inicializado git
git init
git add .
git commit -m "Preparado para producción"

# Crear repositorio en GitHub y subirlo
git remote add origin https://github.com/TU_USUARIO/ysyagenda-django.git
git branch -M main
git push -u origin main
```

### Paso 3: Crear Web Service en Render

1. En el dashboard de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name**: `ysyagenda`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn ysyagenda.wsgi:application`
   - **Plan**: `Free`

### Paso 4: Crear Base de Datos PostgreSQL (Opcional)

1. En Render, clic en **"New +"** → **"PostgreSQL"**
2. **Name**: `ysyagenda-db`
3. **Plan**: `Free`
4. Copia la **Internal Database URL**

### Paso 5: Configurar Variables de Entorno

En la configuración de tu Web Service, ve a **"Environment"** y agrega:

```
SECRET_KEY=tu-secret-key-generada-anteriormente
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com,localhost
DATABASE_URL=postgresql://... (si creaste la DB)
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

### Paso 6: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu app
3. En unos minutos, tu app estará en: `https://tu-app.onrender.com`

### Paso 7: Aplicar Migraciones

Una vez desplegada, ve a la pestaña **"Shell"** en Render y ejecuta:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🚂 Despliegue en Railway

### Paso 1: Crear cuenta

1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con GitHub

### Paso 2: Nuevo Proyecto

1. Clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Elige tu repositorio `ysyagenda-django`

### Paso 3: Agregar PostgreSQL (Opcional)

1. En tu proyecto, clic en **"+ New"**
2. Selecciona **"Database"** → **"PostgreSQL"**
3. Railway automáticamente creará la variable `DATABASE_URL`

### Paso 4: Configurar Variables de Entorno

En **"Variables"**, agrega:

```
SECRET_KEY=tu-secret-key-generada
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}},localhost
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

Railway detectará automáticamente tu `Procfile` y ejecutará el comando de gunicorn.

### Paso 5: Generar Dominio

1. Ve a **"Settings"**
2. En **"Networking"**, clic en **"Generate Domain"**
3. Tu app estará disponible en el dominio generado

---

## 🐍 Despliegue en PythonAnywhere

### Paso 1: Crear cuenta

1. Ve a [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crea una cuenta gratuita

### Paso 2: Subir código

```bash
# En la consola bash de PythonAnywhere
git clone https://github.com/TU_USUARIO/ysyagenda-django.git
cd ysyagenda-django
```

### Paso 3: Crear entorno virtual

```bash
mkvirtualenv --python=/usr/bin/python3.10 ysyagenda
pip install -r requirements.txt
```

### Paso 4: Configurar Web App

1. Ve a la pestaña **"Web"**
2. **"Add a new web app"** → **"Manual configuration"** → **"Python 3.10"**
3. En **"Code"**:
   - **Source code**: `/home/TU_USUARIO/ysyagenda-django`
   - **Working directory**: `/home/TU_USUARIO/ysyagenda-django`
   - **WSGI configuration file**: Editar y pegar:

```python
import os
import sys

path = '/home/TU_USUARIO/ysyagenda-django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ysyagenda.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Paso 5: Configurar entorno virtual

En la pestaña **"Web"**, en **"Virtualenv"**:
- Ruta: `/home/TU_USUARIO/.virtualenvs/ysyagenda`

### Paso 6: Variables de entorno

Crea un archivo `.env` en tu proyecto:

```bash
nano .env
```

Agrega:

```
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=TU_USUARIO.pythonanywhere.com
```

### Paso 7: Archivos estáticos

```bash
python manage.py collectstatic
```

En la pestaña **"Web"**, en **"Static files"**:
- URL: `/static/`
- Directory: `/home/TU_USUARIO/ysyagenda-django/staticfiles`

### Paso 8: Reload

Haz clic en el botón verde **"Reload"** en la pestaña Web.

Tu app estará en: `https://TU_USUARIO.pythonanywhere.com`

---

## ✅ Post-Despliegue

### Verificaciones importantes:

1. **Probar todas las páginas**:
   - Home: `/`
   - Turnos: `/turnos/`
   - Especialidades: `/especialidades/`
   - Profesionales: `/profesionales/`

2. **Verificar conexión con la API**:
   - Verifica que los datos se cargan correctamente
   - Comprueba los filtros en turnos y profesionales

3. **Crear superusuario** (si usas el admin):
   ```bash
   python manage.py createsuperuser
   ```

4. **Monitorear logs**:
   - Render: Pestaña "Logs"
   - Railway: Pestaña "Deployments" → Ver logs
   - PythonAnywhere: Pestaña "Web" → Log files

### Configurar dominio personalizado (Opcional)

Si tienes un dominio propio:

**Render**:
1. Ve a **"Settings"** → **"Custom Domain"**
2. Agrega tu dominio y sigue las instrucciones DNS

**Railway**:
1. Ve a **"Settings"** → **"Networking"** → **"Custom Domain"**
2. Agrega tu dominio

---

## 🔒 Seguridad

### Checklist de seguridad:

- ✅ `DEBUG = False` en producción
- ✅ `SECRET_KEY` única y segura (no la del código)
- ✅ `ALLOWED_HOSTS` configurado correctamente
- ✅ HTTPS habilitado (automático en Render/Railway)
- ✅ Variables de entorno para datos sensibles
- ✅ `.env` en `.gitignore`

---

## 🆘 Solución de Problemas

### Error 500 - Internal Server Error

- Revisa los logs de tu plataforma
- Verifica que `ALLOWED_HOSTS` incluye tu dominio
- Asegúrate de que `DEBUG=False`

### Archivos estáticos no cargan

```bash
python manage.py collectstatic --noinput
```

Verifica que `STATIC_ROOT` está configurado correctamente.

### Base de datos no funciona

- Verifica que `DATABASE_URL` está configurada
- Ejecuta las migraciones: `python manage.py migrate`

### La API no responde

- Verifica que `API_BASE_URL` está configurada correctamente
- Prueba la API directamente: `https://sistemasmdq.com:8443/TurnosCPMI/turnos`

---

## 📚 Recursos Adicionales

- [Documentación de Django - Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Guía de Render para Django](https://render.com/docs/deploy-django)
- [Checklist de despliegue de Django](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

---

## 🎉 ¡Felicitaciones!

Si has seguido esta guía, tu aplicación Django ya debería estar en línea y accesible desde internet.

**Próximos pasos**:
- Compartir la URL con usuarios
- Configurar monitoreo
- Hacer backup de la base de datos
- Configurar dominio personalizado

---

**Desarrollado con ❤️ usando Django & Bootstrap**
