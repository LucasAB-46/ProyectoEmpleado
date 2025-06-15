from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone


class Departamento(models.Model):
    nombre = models.CharField(
        'Nombre del Departamento',
        max_length=50,
        unique=True,
        help_text="Nombre completo del departamento (ej: Recursos Humanos)"
    )
    
    sigla = models.CharField(
        'Sigla',
        max_length=10,
        unique=True,
        help_text="Sigla identificatoria (ej: RRHH)"
    )
    
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        editable=False
    )
    
    activo = models.BooleanField(
        '¿Está activo?',
        default=True,
        help_text="Indica si el departamento está operativo"
    )
    
    piso = models.PositiveSmallIntegerField(
        'Piso',
        blank=True,
        null=True,
        help_text="Número de piso donde se ubica"
    )
    
    oficina = models.CharField(
        'Oficina',
        max_length=10,
        blank=True,
        help_text="Número/identificador de oficina"
    )
    
    fecha_creacion = models.DateTimeField(
        'Fecha de creación',
        auto_now_add=True,
        editable=False
    )
    
    fecha_actualizacion = models.DateTimeField(
        'Fecha de actualización',
        auto_now=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos de la empresa'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['sigla']),
            models.Index(fields=['activo']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'sigla'],
                name='unique_nombre_sigla'
            ),
        ]

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"{self.nombre} ({self.sigla}) - {estado}"

    def clean(self):
        """Validaciones adicionales a nivel de modelo"""
        super().clean()
        
        # Validar que la sigla sea en mayúsculas
        if not self.sigla.isupper():
            raise ValidationError({
                'sigla': "La sigla debe estar en mayúsculas"
            })
            
        # Validar formato de oficina si existe
        if self.oficina and not self.oficina.startswith(('OF-', 'of-', 'OFC-')):
            raise ValidationError({
                'oficina': "El formato debe ser OF-XXX o OFC-XXX"
            })

    def save(self, *args, **kwargs):
        """Generar slug automáticamente antes de guardar"""
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.sigla}")
        
        # Asegurar que la sigla esté en mayúsculas
        self.sigla = self.sigla.upper()
        
        super().save(*args, **kwargs)

    @property
    def ubicacion_completa(self):
        """Devuelve la ubicación formateada"""
        if self.piso and self.oficina:
            return f"Piso {self.piso} - Oficina {self.oficina}"
        elif self.piso:
            return f"Piso {self.piso}"
        elif self.oficina:
            return f"Oficina {self.oficina}"
        return "Sin ubicación asignada"

    def activar(self):
        """Activa el departamento"""
        self.activo = True
        self.save(update_fields=['activo'])

    def desactivar(self):
        """Desactiva el departamento"""
        self.activo = False
        self.save(update_fields=['activo'])

    @classmethod
    def departamentos_activos(cls):
        """Retorna solo los departamentos activos"""
        return cls.objects.filter(activo=True)

    @classmethod
    def crear_departamento(cls, nombre, sigla, piso=None, oficina=None):
        """Método factory para creación consistente"""
        return cls.objects.create(
            nombre=nombre.strip().title(),
            sigla=sigla.strip().upper(),
            piso=piso,
            oficina=oficina
        )