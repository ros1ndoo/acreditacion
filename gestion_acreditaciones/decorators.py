from django.shortcuts import redirect

def usuario_autenticado(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return wrapper
