from atexit import register
from django.contrib import admin
from .models import Empleado,Habilidades

# Register your models here.

admin.site.register(Habilidades)

class EmpleadoAdmin (admin.ModelAdmin):
    list_display = (
        'nombre',
        'apellido',
        'trabajo',
        'departamento',
    )

admin.site.register(Empleado,EmpleadoAdmin)