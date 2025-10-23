import requests
from django.conf import settings
from django.views.generic import TemplateView
from datetime import datetime, timedelta


class HomeView(TemplateView):
    """Vista de página de inicio con información general del sistema"""
    template_name = 'agenda/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'YSY Agenda - Sistema de Gestión de Turnos Médicos'
        return context


class TurnoListView(TemplateView):
    """Vista para mostrar la lista de turnos desde la API con filtros de fecha"""
    template_name = 'agenda/turnos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener filtro de fecha de los parámetros GET
        filtro = self.request.GET.get('filtro', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')

        try:
            # Consumir la API de turnos
            response = requests.get(f'{settings.API_BASE_URL}/turnos', timeout=5)
            if response.status_code == 200:
                turnos = response.json()

                # Guardar el total de turnos sin filtrar
                context['total_turnos'] = len(turnos)

                # Aplicar filtros de fecha
                turnos_filtrados = self._filtrar_turnos_por_fecha(turnos, filtro, fecha_desde, fecha_hasta)
                context['turnos'] = turnos_filtrados
                context['turnos_filtrados'] = len(turnos_filtrados)
                context['filtro_activo'] = filtro
                context['fecha_desde'] = fecha_desde
                context['fecha_hasta'] = fecha_hasta
            else:
                context['turnos'] = []
                context['total_turnos'] = 0
                context['turnos_filtrados'] = 0
                context['error'] = f'Error al obtener turnos: {response.status_code}'
        except requests.exceptions.RequestException as e:
            context['turnos'] = []
            context['total_turnos'] = 0
            context['turnos_filtrados'] = 0
            context['error'] = f'Error de conexion con el backend: {str(e)}'

        return context

    def _filtrar_turnos_por_fecha(self, turnos, filtro, fecha_desde, fecha_hasta):
        """Filtra los turnos según el criterio de fecha seleccionado"""
        if not turnos:
            return []

        ahora = datetime.now()
        hoy_inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        hoy_fin = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)

        turnos_filtrados = []

        for turno in turnos:
            try:
                # Parsear la fecha del turno (formato ISO: 2025-10-22T14:30:00)
                fecha_turno = datetime.fromisoformat(turno['fecha'].replace('Z', '+00:00'))

                if filtro == 'hoy':
                    if hoy_inicio <= fecha_turno <= hoy_fin:
                        turnos_filtrados.append(turno)

                elif filtro == 'manana':
                    manana_inicio = hoy_inicio + timedelta(days=1)
                    manana_fin = hoy_fin + timedelta(days=1)
                    if manana_inicio <= fecha_turno <= manana_fin:
                        turnos_filtrados.append(turno)

                elif filtro == 'semana':
                    # Esta semana (de lunes a domingo)
                    inicio_semana = hoy_inicio - timedelta(days=ahora.weekday())
                    fin_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)
                    if inicio_semana <= fecha_turno <= fin_semana:
                        turnos_filtrados.append(turno)

                elif filtro == 'mes':
                    # Este mes
                    if fecha_turno.year == ahora.year and fecha_turno.month == ahora.month:
                        turnos_filtrados.append(turno)

                elif filtro == 'rango' and fecha_desde and fecha_hasta:
                    # Rango personalizado
                    try:
                        fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
                        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                        if fecha_desde_dt <= fecha_turno <= fecha_hasta_dt:
                            turnos_filtrados.append(turno)
                    except ValueError:
                        turnos_filtrados.append(turno)
                else:
                    # Sin filtro, mostrar todos
                    turnos_filtrados.append(turno)

            except (ValueError, KeyError):
                # Si hay error al parsear la fecha, incluir el turno de todas formas
                turnos_filtrados.append(turno)

        return turnos_filtrados


class EspecialidadListView(TemplateView):
    """Vista para mostrar la lista de especialidades desde la API"""
    template_name = 'agenda/especialidades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Consumir la API de especialidades
            response = requests.get(f'{settings.API_BASE_URL}/especialidades', timeout=5)
            if response.status_code == 200:
                context['especialidades'] = response.json()
            else:
                context['especialidades'] = []
                context['error'] = f'Error al obtener especialidades: {response.status_code}'
        except requests.exceptions.RequestException as e:
            context['especialidades'] = []
            context['error'] = f'Error de conexión con el backend: {str(e)}'

        return context


class ProfesionalListView(TemplateView):
    """Vista para mostrar la lista de profesionales desde la API con filtros"""
    template_name = 'agenda/profesionales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener filtros de los parámetros GET
        especialidad_filtro = self.request.GET.get('especialidad', '')
        busqueda = self.request.GET.get('busqueda', '').strip()

        try:
            # Consumir la API de usuarios filtrando por tipo PROFESIONAL
            response = requests.get(
                f'{settings.API_BASE_URL}/usuarios',
                params={'tipo': 'PROFESIONAL'},
                timeout=5
            )

            # Consumir la API de especialidades para el dropdown
            response_especialidades = requests.get(
                f'{settings.API_BASE_URL}/especialidades',
                timeout=5
            )

            if response.status_code == 200:
                profesionales = response.json()

                # Guardar el total de profesionales sin filtrar
                context['total_profesionales'] = len(profesionales)

                # Aplicar filtros
                profesionales_filtrados = self._filtrar_profesionales(
                    profesionales, especialidad_filtro, busqueda
                )

                context['profesionales'] = profesionales_filtrados
                context['profesionales_filtrados'] = len(profesionales_filtrados)
                context['especialidad_filtro'] = especialidad_filtro
                context['busqueda'] = busqueda

                # Agregar lista de especialidades para el filtro
                if response_especialidades.status_code == 200:
                    context['especialidades'] = response_especialidades.json()
                else:
                    context['especialidades'] = []
            else:
                context['profesionales'] = []
                context['total_profesionales'] = 0
                context['profesionales_filtrados'] = 0
                context['especialidades'] = []
                context['error'] = f'Error al obtener profesionales: {response.status_code}'
        except requests.exceptions.RequestException as e:
            context['profesionales'] = []
            context['total_profesionales'] = 0
            context['profesionales_filtrados'] = 0
            context['especialidades'] = []
            context['error'] = f'Error de conexion con el backend: {str(e)}'

        return context

    def _filtrar_profesionales(self, profesionales, especialidad_filtro, busqueda):
        """Filtra profesionales por especialidad y búsqueda por nombre/apellido"""
        if not profesionales:
            return []

        profesionales_filtrados = []

        for profesional in profesionales:
            # Filtro por especialidad
            if especialidad_filtro:
                especialidad_prof = profesional.get('especialidad', '').lower()
                if especialidad_filtro.lower() not in especialidad_prof:
                    continue

            # Filtro por búsqueda en nombre o apellido
            if busqueda:
                nombre_completo = f"{profesional.get('nombre', '')} {profesional.get('apellido', '')}".lower()
                if busqueda.lower() not in nombre_completo:
                    continue

            profesionales_filtrados.append(profesional)

        return profesionales_filtrados
