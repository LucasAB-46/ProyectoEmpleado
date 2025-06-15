from django.shortcuts import render
from django.views.generic import ListView
from .models import Departamento

class DepartamentoListView(ListView):
    model = Departamento
    template_name = 'departamento/departamento_list.html'  # Ruta del template
    context_object_name = 'departamentos'
    paginate_by = 10  

    def get_queryset(self):
        """Podés personalizar el queryset si querés filtrar departamentos activos, por ejemplo"""
        return Departamento.objects.filter(activo=True).order_by('nombre')
