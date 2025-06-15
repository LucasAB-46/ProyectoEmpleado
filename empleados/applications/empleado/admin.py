from datetime import date

from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Empleado, Habilidades, Pais




# Formulario personalizado para Empleado con CKEditor 5
class EmpleadoAdminForm(forms.ModelForm):
    """Formulario personalizado para el modelo Empleado."""
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'observaciones': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="default"
            )
        }


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = (
        'nombre',
        'apellido',
        'fecha_nac',
        'calcular_edad',
        'pais',
        'puesto',
        'departamento',
        
    )
    search_fields = (
        'apellido',
        'nombre',
    )
    list_filter = (
        'departamento',
        'puesto',
        'pais',
        'habilidades',
    )
    filter_horizontal = ('habilidades',)

    def calcular_edad(self, obj):
        if not obj.fecha_nac:
            return "Fecha no especificada"
        today = date.today()
        edad = today.year - obj.fecha_nac.year - (
            (today.month, today.day) < (obj.fecha_nac.month, obj.fecha_nac.day)
        )
        return f"{edad} años"

    calcular_edad.short_description = 'Edad'
    calcular_edad.admin_order_field = 'fecha_nac'

   

   


# Registro de los demás modelos
admin.site.register(Habilidades)
admin.site.register(Pais)


