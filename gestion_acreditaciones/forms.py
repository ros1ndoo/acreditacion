import re
from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Centro




class UsuarioRegistroForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Contraseña",
        help_text="Debe tener al menos 8 caracteres, incluyendo un número y una letra mayúscula."
    )
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'contrasena', 'rol']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': 'required'}),
            'correo_electronico': forms.EmailInput(attrs={'required': 'required'}),
        }
        labels = {
            'correo_electronico': 'Correo Electrónico',
        }

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")
        nombre = cleaned_data.get("nombre")
        correo = cleaned_data.get("correo_electronico")
        errores = []

        # Validación de campos vacíos
        if not nombre:
            errores.append("El campo 'Nombre' no puede estar vacío.")
        if not correo:
            errores.append("El campo 'Correo Electrónico' no puede estar vacío.")
        if not contrasena:
            errores.append("El campo 'Contraseña' no puede estar vacío.")
        if not confirmar_contrasena:
            errores.append("El campo 'Confirmar Contraseña' no puede estar vacío.")

        # Validación de coincidencia de contraseñas
        if contrasena and confirmar_contrasena and contrasena != confirmar_contrasena:
            errores.append("Las contraseñas no coinciden.")

        # Validación de la complejidad de la contraseña
        if contrasena:
            if len(contrasena) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres.")
            if not any(char.isdigit() for char in contrasena):
                errores.append("La contraseña debe contener al menos un número.")
            if not any(char.isupper() for char in contrasena):
                errores.append("La contraseña debe contener al menos una letra mayúscula.")

        # Si hay errores, lanza una excepción
        if errores:
            raise ValidationError(errores)

        # Encriptar la contraseña antes de guardar
        cleaned_data['contrasena'] = make_password(contrasena)
        return cleaned_data

class UsuarioLoginForm(forms.Form):
    correo_electronico = forms.EmailField(label='Correo Electrónico')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class CentroForm(forms.ModelForm):
    class Meta:
        model = Centro
        fields = ['nombre_centro', 'codigo_centro', 'direccion', 'contacto']
