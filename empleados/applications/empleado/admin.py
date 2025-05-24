from django.contrib import admin
from .models import Empleado, Habilidades, Pais
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from datetime import date

# Formulario personalizado para Empleado con CKEditor 5
class EmpleadoAdminForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'observaciones': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="default"
            )
        } 

admin.site.register(Habilidades)

class EmpleadoAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm 
    list_display = (
        'nombre',
        'apellido',
        'fecha_nac',
        'calcular_edad',
        'pais',
        'trabajo',
        'departamento',
    )

    def calcular_edad(self, obj):
        """
        Calcula la edad del empleado basado en su fecha de nacimiento
        Devuelve 'Fecha no especificada' si no tiene fecha registrada
        """
        if obj.fecha_nac is None:
            return "Fecha no especificada"
        
        today = date.today()
        edad = today.year - obj.fecha_nac.year - ((today.month, today.day) < (obj.fecha_nac.month, obj.fecha_nac.day))
        return f"{edad} años"
    
    calcular_edad.short_description = 'Edad'
    calcular_edad.admin_order_field = 'fecha_nac'
    
    search_fields = (
        'apellido',
        'nombre',
    )

    list_filter = (
        'departamento',
        'trabajo',
        'pais',
        'habilidades',
    )

    filter_horizontal = (
        'habilidades',
    )

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Pais)