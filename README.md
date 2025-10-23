# YSY Agenda - Sistema de Gestión de Turnos Médicos

![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

## Descripción

YSY Agenda es una aplicación web desarrollada con Django que permite visualizar y gestionar turnos médicos, especialidades y profesionales de la salud. La aplicación consume una API REST desarrollada en Java (Spring Boot) y presenta la información de manera clara y organizada utilizando Bootstrap 5.

Este proyecto fue desarrollado como Proyecto Final de la materia "Introducción a la Programación Web con Django".

## Características

- **Vistas Basadas en Clases (CBV)**: Implementación de vistas utilizando `TemplateView` de Django
- **Herencia de Plantillas**: Uso de `base.html` como template padre y templates hijos para cada vista
- **Bootstrap 5**: Diseño responsivo y moderno con componentes de Bootstrap 5
- **Consumo de API REST**: Integración con backend Java para obtener datos dinámicos
- **Manejo de Errores**: Mensajes informativos cuando el backend no está disponible
- **Navegación Intuitiva**: Navbar con enlaces a todas las secciones

## Funcionalidades

### Página de Inicio
- Vista general del sistema
- Tarjetas informativas para acceder a cada sección
- Información sobre las características del proyecto

### Turnos
- Lista completa de turnos médicos programados
- Muestra información del paciente y profesional
- Especialidad y fecha/hora del turno
- Tabla responsiva con todos los detalles

### Especialidades
- Catálogo de especialidades médicas disponibles
- Vista en tarjetas (cards) con diseño atractivo
- Contador de especialidades disponibles

### Profesionales
- Directorio de profesionales de la salud
- Información de contacto (email, teléfono, DNI)
- Especialidad de cada profesional
- Avatar con iniciales y color personalizado

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Backend Java ejecutándose en `http://localhost:8080` (opcional para pruebas)
- MySQL con la base de datos `ysyagenda` configurada (para el backend)

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/ysyagenda-django.git
cd ysyagenda-django
```

### 2. Crear y activar un entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar las migraciones

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## Configuración del Backend

Para que la aplicación funcione correctamente, necesitas tener el backend de Java ejecutándose:

1. Navega al directorio del backend Java
2. Asegúrate de que MySQL esté ejecutándose
3. Ejecuta el backend (generalmente en el puerto 8080)

Si el backend no está disponible, la aplicación mostrará mensajes informativos en lugar de errores.

## Estructura del Proyecto

```
ysyagenda-django/
├── agenda/                      # Aplicación principal
│   ├── templates/              # Plantillas HTML
│   │   ├── base.html          # Plantilla base
│   │   └── agenda/            # Templates de la app
│   │       ├── home.html
│   │       ├── turnos.html
│   │       ├── especialidades.html
│   │       └── profesionales.html
│   ├── views.py               # Vistas basadas en clases
│   ├── urls.py                # URLs de la aplicación
│   └── ...
├── ysyagenda/                 # Configuración del proyecto
│   ├── settings.py           # Configuración general
│   ├── urls.py               # URLs principales
│   └── ...
├── manage.py                 # Script de gestión de Django
├── requirements.txt          # Dependencias del proyecto
└── README.md                # Este archivo
```

## Endpoints Consumidos del Backend

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/turnos` | GET | Lista de todos los turnos |
| `/especialidades` | GET | Lista de todas las especialidades |
| `/usuarios?tipo=PROFESIONAL` | GET | Lista de profesionales |

**Base URL del Backend:** `http://localhost:8080`

## Tecnologías Utilizadas

- **Django 5.2.7**: Framework web de Python
- **Bootstrap 5.3.0**: Framework CSS para diseño responsivo
- **Bootstrap Icons**: Iconos para mejorar la interfaz
- **Requests**: Librería de Python para consumir APIs REST
- **Python 3.x**: Lenguaje de programación

## Características Técnicas Destacadas

### Vistas Basadas en Clases (CBV)
El proyecto utiliza `TemplateView` para implementar vistas limpias y reutilizables:

```python
class TurnoListView(TemplateView):
    template_name = 'agenda/turnos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Consumo de API
        response = requests.get(f'{settings.API_BASE_URL}/turnos')
        context['turnos'] = response.json()
        return context
```

### Herencia de Plantillas
Todas las páginas heredan de `base.html`, promoviendo la reutilización de código:

```django
{% extends 'base.html' %}

{% block title %}Turnos - YSY Agenda{% endblock %}

{% block content %}
    <!-- Contenido específico -->
{% endblock %}
```

### Manejo de Errores
Implementación de try-except para manejar errores de conexión con el backend:

```python
try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        context['data'] = response.json()
except requests.exceptions.RequestException as e:
    context['error'] = str(e)
```

## Autor

**Tu Nombre**
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)
- Email: tu.email@ejemplo.com

## Proyecto Final

Este proyecto fue desarrollado como parte del curso "Introducción a la Programación Web con Django" y cumple con los siguientes requisitos:

- ✅ Proyecto Django funcional
- ✅ Aplicación creada con `startapp`
- ✅ Configuración correcta de settings.py, urls.py, views.py
- ✅ Uso de Bootstrap 5
- ✅ Herencia de plantillas (base.html + templates hijos)
- ✅ Vistas basadas en clases (CBV)
- ✅ Información dinámica desde API
- ✅ Manejo de contexto en vistas
- ✅ Repositorio en GitHub
- ✅ README.md completo

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

---

**Desarrollado con Django & Bootstrap** 🚀
