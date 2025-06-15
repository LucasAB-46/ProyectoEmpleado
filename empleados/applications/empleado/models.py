from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field
from applications.departamento.models import Departamento

class Pais(models.Model):
    nombre = models.CharField('Nombre del país', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Habilidades(models.Model):
    habilidad = models.CharField('Habilidad', max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['habilidad']

    def __str__(self):
        return self.habilidad

class Empleado(models.Model):
    PUESTOS = (
        ('0', 'Contador'),
        ('1', 'Administrativo'),
        ('2', 'Desarrollador'),
        ('3', 'Analista'),
        ('4', 'Gerente'),
        ('9', 'Otro'),
    )

    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    fecha_nac = models.DateField('Fecha de nacimiento', null=True, blank=True)
    puesto = models.CharField('Puesto', max_length=2, choices=PUESTOS)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    habilidades = models.ManyToManyField(Habilidades, blank=True)
    observaciones = CKEditor5Field('Observaciones', config_name='default', blank=True, null=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['apellido', 'nombre']
        unique_together = ('nombre', 'apellido', 'departamento')

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'

    def clean(self):
        if self.fecha_nac and self.fecha_nac > date.today():
            raise ValidationError("Fecha de nacimiento no puede ser futura")

    @property
    def edad(self):
        if not self.fecha_nac:
            return None
        today = date.today()
        return today.year - self.fecha_nac.year - ((today.month, today.day) < (self.fecha_nac.month, self.fecha_nac.day))



