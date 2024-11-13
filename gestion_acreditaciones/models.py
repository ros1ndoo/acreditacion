from django.db import models

# Modelo para Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)  
    rol = models.CharField(max_length=50, choices=[('Admin', 'Administrador'), ('Centro', 'Responsable de Centro')])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Modelo para Centros
class Centro(models.Model):
    nombre_centro = models.CharField(max_length=100)
    codigo_centro = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    contacto = models.CharField(max_length=50, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_centro

# Modelo para Planes de Estudio
class PlanDeEstudio(models.Model):
    nombre_plan = models.CharField(max_length=100)
    codigo_plan = models.CharField(max_length=20)
    centro_asociado = models.ForeignKey(Centro, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_acreditacion = models.DateField(null=True, blank=True)
    fecha_proxima_acreditacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre_plan

# Modelo para Acreditaciones
class Acreditacion(models.Model):
    plan_estudio = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada'), ('Rechazada', 'Rechazada')])
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Acreditación de {self.plan_estudio}"

# Modelo para Historial de Cambios (opcional)
class HistorialCambio(models.Model):
    entidad_modificada = models.CharField(max_length=50)
    tipo_cambio = models.CharField(max_length=50, choices=[('Creación', 'Creación'), ('Modificación', 'Modificación'), ('Eliminación', 'Eliminación')])
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    detalles_cambio = models.TextField()

    def __str__(self):
        return f"Cambio en {self.entidad_modificada} por {self.usuario}"
