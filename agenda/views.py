import requests
from django.conf import settings
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Vista de página de inicio con información general del sistema"""
    template_name = 'agenda/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'YSY Agenda - Sistema de Gestión de Turnos Médicos'
        return context


class TurnoListView(TemplateView):
    """Vista para mostrar la lista de turnos desde la API"""
    template_name = 'agenda/turnos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Consumir la API de turnos
            response = requests.get(f'{settings.API_BASE_URL}/turnos', timeout=5)
            if response.status_code == 200:
                context['turnos'] = response.json()
            else:
                context['turnos'] = []
                context['error'] = f'Error al obtener turnos: {response.status_code}'
        except requests.exceptions.RequestException as e:
            context['turnos'] = []
            context['error'] = f'Error de conexión con el backend: {str(e)}'

        return context


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
    """Vista para mostrar la lista de profesionales desde la API"""
    template_name = 'agenda/profesionales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Consumir la API de usuarios filtrando por tipo PROFESIONAL
            response = requests.get(
                f'{settings.API_BASE_URL}/usuarios',
                params={'tipo': 'PROFESIONAL'},
                timeout=5
            )
            if response.status_code == 200:
                context['profesionales'] = response.json()
            else:
                context['profesionales'] = []
                context['error'] = f'Error al obtener profesionales: {response.status_code}'
        except requests.exceptions.RequestException as e:
            context['profesionales'] = []
            context['error'] = f'Error de conexión con el backend: {str(e)}'

        return context
