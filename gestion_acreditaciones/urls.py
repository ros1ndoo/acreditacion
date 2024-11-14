from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Ruta para la URL raíz (login por defecto)
    path('acreditacion-centros/', views.acreditacion_centros_view, name='acreditacion_centros'),
    path('acreditacion-estudios/', views.acreditacion_estudios_view, name='acreditacion_estudios'),
    path('periodos-evaluacion/', views.periodos_evaluacion_view, name='periodos_evaluacion'),
    path('main/', views.main_view, name='main'),  # Cambia la vista principal a una URL diferente si es necesario
]
