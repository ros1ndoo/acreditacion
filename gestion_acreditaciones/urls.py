from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='root_login'),  # Ruta para la URL raíz (login por defecto)
    path('acreditacion-estudios/', views.acreditacion_estudios_view, name='acreditacion_estudios'),
    path('periodos-evaluacion/', views.periodos_evaluacion_view, name='periodos_evaluacion'),
    path('main/', views.main_view, name='main'),  # Ruta para la vista principal
    path('registro/', views.registro_usuario, name='registro'),  # Ruta para el registro de usuarios
    path('login/', views.login_usuario, name='login'),  # Ruta para el inicio de sesión
    path('logout/', views.logout_usuario, name='logout'),  # Ruta para cerrar sesión
    path('centros/', views.listar_centros, name='listar_centros'),  # Ruta para listar centros
    path('acreditacion-centros/', views.listar_centros, name='listar_acreditacion_centros'),  # Ruta para la acreditación de centros
    path('descargar_centros/', views.descargar_centros_csv, name='descargar_centros'),  # Ruta para descargar centros en formato CSV
    path('descargar_planes_estudio/', views.descargar_planes_estudio_csv, name='descargar_planes_estudio'),  # Ruta para descargar planes de estudio en formato CSV
    path('descargar_acreditaciones/', views.descargar_acreditaciones_csv, name='descargar_acreditaciones'),  # Ruta para descargar acreditaciones en formato CSV
    path('listar_periodos_evaluacion/', views.listar_periodos_evaluacion, name='listar_periodos_evaluacion'),  # Ruta para listar periodos de evaluación
    path('listar_estudios/', views.listar_estudios, name='listar_estudios'),  # Ruta para listar estudios
    path('descargar_periodos_evaluacion/', views.descargar_periodos_evaluacion_csv, name='descargar_periodos_evaluacion'),  # Ruta para descargar periodos de evaluación en formato CSV
]