from django.db import models
from datetime import date 
from applications.departamento.models import Departamento 
from django_ckeditor_5.fields import CKEditor5Field

class Pais(models.Model):
    nombre = models.CharField('Nombre del país', max_length=100)
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        
    def __str__(self):
        return self.nombre

class Habilidades(models.Model):
    habilidad = models.CharField('Habilidad', max_length=50)

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades del empleado'
        ordering = ['habilidad']
        unique_together = ('habilidad',)

    def __str__(self):
        return self.habilidad

class Empleado(models.Model):
    JOB_CHOICES = (
        ('0', 'Contador'),
        ('1', 'Administrativo'),
        ('2', 'Desarrollador'),
        ('3', 'Analista Funcional'),
        ('4', 'Otro'),
    )
    
    nombre = models.CharField('Nombre', max_length=60)
    apellido = models.CharField('Apellido', max_length=60)
    fecha_nac = models.DateField('Fecha de Nacimiento', null=True, blank=True) 
    trabajo = models.CharField('Trabajo', max_length=50, choices=JOB_CHOICES)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    habilidades = models.ManyToManyField(Habilidades)
    observaciones = CKEditor5Field('Texto de Observacion', config_name='default', blank=True, null=True)

    class Meta:
        verbose_name = 'Mi empleado'
        verbose_name_plural = 'Empleados de la empresa'
        ordering = ['-nombre', 'apellido']
        unique_together = ('nombre', 'departamento')

    def __str__(self):
        return f'{self.nombre} - {self.apellido}'