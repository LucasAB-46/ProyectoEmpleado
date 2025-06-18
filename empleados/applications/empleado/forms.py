from django import forms
from .models import Empleado, Habilidades, Pais
from applications.departamento.models import Departamento
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

class EmpleadoForm(forms.ModelForm):
    habilidades = forms.ModelMultipleChoiceField(

        
        queryset=Habilidades.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Habilidades del empleado"
    )

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'puesto', 'departamento', 'pais', 'fecha_nac', 'habilidades', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pérez'
            }),
            'puesto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'pais': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un país'
            }),
            'fecha_nac': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': timezone.now().date().isoformat()
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones relevantes sobre el empleado'
            }),
        }
        labels = {
            'puesto': "Puesto de Trabajo",
            'departamento': "Departamento",
            'pais': "País",
            'fecha_nac': "Fecha de Nacimiento"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos departamentos activos
        self.fields['departamento'].queryset = Departamento.objects.filter(activo=True)
        
        # Ordenamos países alfabéticamente
        self.fields['pais'].queryset = Pais.objects.all().order_by('nombre')
        
        # Si estamos editando, cargamos las habilidades actuales
        if self.instance.pk:
            self.fields['habilidades'].initial = self.instance.habilidades.all()

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres")
        return nombre.capitalize()

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()
        if len(apellido) < 2:
            raise ValidationError("El apellido debe tener al menos 2 caracteres")
        return apellido.capitalize()

    def clean_fecha_nac(self):
        fecha_nac = self.cleaned_data['fecha_nac']
        if fecha_nac:
            edad = (date.today() - fecha_nac).days // 365
            if edad < 18:
                raise ValidationError("El empleado debe ser mayor de edad")
            if edad > 100:
                raise ValidationError("Por favor verifique la fecha de nacimiento")
        return fecha_nac

    def save(self, commit=True):
        empleado = super().save(commit=False)
        if commit:
            empleado.save()
            self.save_m2m()  # Necesario para guardar las relaciones ManyToMany
            empleado.habilidades.set(self.cleaned_data['habilidades'])
        return empleado

""" 
El método __init__ personalizado sirve para modificar el formulario en tiempo de ejecución, después de que Django ya hizo la construcción inicial.
Siempre que lo sobrescriban, tienen que llamar primero a super().__init__() para que el formulario se inicialice bien. 
"""