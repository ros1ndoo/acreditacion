from django.shortcuts import render

def main_view(request):
    return render(request, 'main.html')

def acreditacion_centros_view(request):
    return render(request, 'acreditacion_centros.html')

def acreditacion_estudios_view(request):
    return render(request, 'acreditacion_estudios.html')

def periodos_evaluacion_view(request):
    return render(request, 'periodos_evaluacion.html')

def login_view(request):
    return render(request, 'login.html')
