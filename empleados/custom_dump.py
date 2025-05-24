import json
from django.core import serializers
from django.apps import apps
import codecs

def export_safe():
    """Exporta datos manejando caracteres no-UTF8"""
    data = {}
    for model in apps.get_models():
        try:
            # Convierte todos los valores a string para evitar errores
            data[model._meta.label] = [
                {k: str(v) if v is not None else None for k, v in obj.items()}
                for obj in model.objects.all().values()
            ]
        except Exception as e:
            print(f"[!] Omitiendo {model._meta.label}: {str(e)}")
            continue
    
    # Guarda con reemplazo de caracteres inválidos (�)
    with codecs.open('datadump_fixed.json', 'w', encoding='utf-8', errors='replace') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("[✓] Datos exportados en datadump_fixed.json")

if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empleados.settings')  # Reemplaza 'empleados' con tu nombre de proyecto
    import django
    django.setup()
    export_safe()