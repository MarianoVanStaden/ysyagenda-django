from django.urls import path
from .views import HomeView, TurnoListView, EspecialidadListView, ProfesionalListView

app_name = 'agenda'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('turnos/', TurnoListView.as_view(), name='turnos'),
    path('especialidades/', EspecialidadListView.as_view(), name='especialidades'),
    path('profesionales/', ProfesionalListView.as_view(), name='profesionales'),
]
