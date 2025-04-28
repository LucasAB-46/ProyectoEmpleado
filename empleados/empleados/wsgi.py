"""
WSGI config for empleados project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Ruta base del proyecto (ajustado para estructura profesional)
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Configuración para entornos múltiples
SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if not SETTINGS_MODULE:
    # Valor por defecto para desarrollo (cambiar en producción)
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'empleados.settings.local'  # Asume estructura settings/ separada
    )

# 2. Carga la aplicación WSGI
application = get_wsgi_application()

# 3. Opcional: Configuración para WhiteNoise (archivos estáticos)
try:
    from whitenoise import WhiteNoise
    application = WhiteNoise(
        application,
        root=os.path.join(BASE_DIR, 'staticfiles'),
        prefix='static/'
    )
except ImportError:
    pass  # Solo aplica en producción
