from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UsuarioLoginForm, UsuarioRegistroForm, CentroForm
from .models import Acreditacion, Centro, PlanDeEstudio, Usuario, PeriodoEvaluacion
from .decorators import usuario_autenticado
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password


import csv
from django.http import HttpResponse

def tablaCSV(queryset, model_name):
    """
    Exporta un queryset como un archivo CSV.
    :param queryset: El conjunto de datos (queryset) que se exportará.
    :param model_name: El nombre del modelo o de la tabla que se exporta.
    :return: HttpResponse con el archivo CSV adjunto.
    """
    field_names = [field.name for field in queryset.model._meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_data.csv"'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)
    return response

@usuario_autenticado
def descargar_centros_csv(request):
    queryset = Centro.objects.all()
    return tablaCSV(queryset, 'centro')

@usuario_autenticado
def descargar_planes_estudio_csv(request):
    queryset = PlanDeEstudio.objects.all()  # Utiliza el modelo PlanDeEstudio
    return tablaCSV(queryset, 'plan_de_estudio')


@usuario_autenticado
def descargar_acreditaciones_csv(request):
    queryset = Acreditacion.objects.all()  # Utiliza el modelo Acreditacion
    return tablaCSV(queryset, 'acreditacion')

@usuario_autenticado
def main_view(request):
    return render(request, 'main.html')

@usuario_autenticado
def acreditacion_centros_view(request):
    return render(request, 'acreditacion_centros.html')

@usuario_autenticado
def acreditacion_estudios_view(request):
    return render(request, 'acreditacion_estudios.html')

@usuario_autenticado
def periodos_evaluacion_view(request):
    return render(request, 'periodos_evaluacion.html')

def login_view(request):
    # Si el usuario ya ha iniciado sesión, redirigirlo a 'main'
    if 'usuario_id' in request.session:
        return redirect('main')  # Redirige a la vista 'main' si el usuario ya está autenticado
    
    # Si el usuario no ha iniciado sesión, muestra la página de inicio de sesión
    return render(request, 'login.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro completado con éxito. Ahora puedes iniciar sesión.')
            return redirect('login')  
        else:
            messages.error(request, 'Por favor corrige los errores indicados en el formulario.')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            correo_electronico = form.cleaned_data['correo_electronico']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(correo_electronico=correo_electronico)
                # Verificar la contraseña
                if check_password(contrasena, usuario.contrasena):
                    request.session['usuario_id'] = usuario.pk
                    request.session['usuario_nombre'] = usuario.nombre
                    messages.success(request, f'Bienvenido, {usuario.nombre}!')
                    return redirect('main')
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
    else:
        form = UsuarioLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    logout(request)  
    return redirect('login')

@usuario_autenticado
def listar_centros(request):
    # Recuperar todos los centros
    centros = Centro.objects.all()
    editar_centro = None

    if request.method == 'POST':
        accion = request.POST.get('accion')

        # Manejar edición de un centro existente
        if accion and accion.startswith('editar_'):
            id = accion.split('_')[-1]
            try:
                editar_centro = Centro.objects.get(pk=id)
            except Centro.DoesNotExist:
                messages.error(request, f'No se pudo encontrar el centro con ID {id}.')

        # Manejar guardar cambios de un centro existente
        elif accion and accion.startswith('guardar_'):
            id = accion.split('_')[-1]
            try:
                centro = Centro.objects.get(pk=id)
                centro.nombre_centro = request.POST.get('nombre_centro', centro.nombre_centro).strip()
                centro.codigo_centro = request.POST.get('codigo_centro', centro.codigo_centro).strip()
                centro.direccion = request.POST.get('direccion', centro.direccion).strip()
                centro.contacto = request.POST.get('contacto', centro.contacto).strip()
                centro.save()
                messages.success(request, f'Centro "{centro.nombre_centro}" actualizado con éxito.')
                return redirect('acreditacion-centros')
            except Centro.DoesNotExist:
                messages.error(request, f'No se pudo encontrar el centro con ID {id}.')

        # Manejar eliminación de un centro existente
        elif accion and accion.startswith('eliminar_'):
            id = accion.split('_')[-1]
            try:
                centro = Centro.objects.get(pk=id)
                centro.delete()
                messages.success(request, f'Centro "{centro.nombre_centro}" eliminado con éxito.')
                return redirect('acreditacion-centros')
            except Centro.DoesNotExist:
                messages.error(request, f'No se pudo encontrar el centro con ID {id}.')

    return render(request, 'acreditacion_centros.html', {'centros': centros, 'editar_centro': editar_centro})

@usuario_autenticado
def listar_estudios(request):
    estudios = PlanDeEstudio.objects.all()
    total_items = estudios.count()
    return render(request, 'acreditacion_estudios.html', {'estudios': estudios, 'total_items': total_items})

@usuario_autenticado
def listar_periodos_evaluacion(request):
    periodos = PeriodoEvaluacion.objects.all()
    total_items = periodos.count()
    return render(request, 'listar_periodos_evaluacion.html', {'periodos': periodos, 'total_items': total_items})

@usuario_autenticado
def descargar_periodos_evaluacion_csv(request):
    periodos = PeriodoEvaluacion.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="periodos_evaluacion.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Fecha de Inicio', 'Fecha de Fin'])

    for periodo in periodos:
        writer.writerow([periodo.id, periodo.nombre, periodo.fecha_inicio, periodo.fecha_fin])

    return response

