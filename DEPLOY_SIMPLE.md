# 🚀 DESPLIEGUE SIMPLE - Frontend Django

## Tu Situación
✅ Backend Java funcionando en: `https://sistemasmdq.com:8443/TurnosCPMI`  
✅ Este proyecto Django solo consume las APIs  
✅ No necesitas base de datos externa (usas SQLite)  
✅ Solo necesitas subir el frontend a internet  

---

## 🎯 3 PASOS PARA SUBIR A INTERNET

### PASO 1: Instalar Dependencias Mínimas

```powershell
pip install python-dotenv whitenoise gunicorn
```

### PASO 2: Generar SECRET_KEY

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copia y guarda el resultado** (lo usarás en el Paso 3)

### PASO 3: Subir a Render (GRATIS)

#### 3.1 Subir código a GitHub

```powershell
git add .
git commit -m "Listo para producción"
git push origin main
```

#### 3.2 Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub

#### 3.3 Crear Web Service

1. En Render, clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio: `ysyagenda-django`
3. Configura:

| Campo | Valor |
|-------|-------|
| **Name** | `ysyagenda` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn ysyagenda.wsgi:application` |
| **Plan** | `Free` |

4. Haz clic en **"Advanced"** y agrega las **Variables de Entorno**:

```
SECRET_KEY=tu-secret-key-generada-en-paso-2
DEBUG=False
ALLOWED_HOSTS=.onrender.com
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
PYTHON_VERSION=3.11.0
```

5. Clic en **"Create Web Service"**

#### 3.4 Esperar el despliegue

- Render tardará 2-5 minutos en construir y desplegar
- Verás los logs en tiempo real
- Cuando termine, tu app estará en: `https://ysyagenda.onrender.com`

---

## ✅ Verificar que Funciona

Visita estas URLs:

- **Home**: `https://tu-app.onrender.com/`
- **Turnos**: `https://tu-app.onrender.com/turnos/`
- **Especialidades**: `https://tu-app.onrender.com/especialidades/`
- **Profesionales**: `https://tu-app.onrender.com/profesionales/`

Deberías ver todos los datos del backend Java funcionando correctamente.

---

## ⚡ Alternativas Rápidas

### Railway (también GRATIS)

1. Ve a [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub**
3. Selecciona tu repositorio
4. En **Variables**, agrega las mismas del Paso 3.4
5. Railway detecta automáticamente el `Procfile`

### PythonAnywhere (GRATIS básico)

Ver guía completa en `DEPLOYMENT.md`

---

## 🔧 Comandos Útiles

```powershell
# Probar localmente antes de subir
python manage.py runserver

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Probar con gunicorn (como en producción)
gunicorn ysyagenda.wsgi:application
```

---

## 📝 Notas Importantes

### ⚠️ Plan Gratuito de Render:
- ✅ Tu app estará disponible 24/7
- ⚠️ Se "duerme" después de 15 min sin actividad
- ⏱️ Primer acceso después de dormir: 30-60 segundos
- 💡 Solución: Usar cron job gratuito para mantenerla activa

### 🔄 Actualizar la Aplicación:

Cada vez que hagas cambios:

```powershell
git add .
git commit -m "Descripción de cambios"
git push origin main
```

Render detectará el cambio y redesplegar automáticamente.

### 🌐 Dominio Personalizado:

Si tienes tu propio dominio:
1. En Render → **Settings** → **Custom Domain**
2. Agrega tu dominio
3. Configura los DNS según indicaciones

---

## 🆘 Solución de Problemas

### Error 500 en Render

Revisa los logs en Render → **Logs**

Causa común:
- `ALLOWED_HOSTS` mal configurado
- `SECRET_KEY` no configurada

### La API no responde

Verifica que `API_BASE_URL` esté configurada:
```
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
```

### Archivos estáticos no cargan

En Render, verifica que el Build Command incluya:
```
python manage.py collectstatic --noinput
```

---

## 🎉 ¡Eso es Todo!

Tu aplicación Django estará consumiendo las APIs de tu backend Java y funcionando en internet.

**Tiempo estimado**: 15-20 minutos ⏱️

---

## 🔗 Variables de Entorno - Referencia Rápida

Para copiar/pegar en Render o Railway:

```
SECRET_KEY=genera-una-nueva-con-el-comando-del-paso-2
DEBUG=False
ALLOWED_HOSTS=.onrender.com
API_BASE_URL=https://sistemasmdq.com:8443/TurnosCPMI
PYTHON_VERSION=3.11.0
```

**IMPORTANTE**: Reemplaza `SECRET_KEY` con la que generaste en el Paso 2.

---

¿Listo para desplegar? ¡Sigue los 3 pasos y estarás en línea! 🚀
