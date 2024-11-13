from django.contrib import admin
from django.urls import path
from . import views  # Asegúrate de importar las vistas de tu aplicación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test_page, name='test_page'),  # Ruta para la página de prueba
    path('', views.test_page, name='home'),  # Ruta para la página de inicio
]
