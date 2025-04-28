from django.shortcuts import render
# uso una vista generica de django 
from django.views.generic import TemplateView, ListView
from .models import Empleado

class IndexView (TemplateView):
    template_name= 'empleado/home.html' # lo debemos crear en la carpeta templates

    # Opcional: Añadir contexto dinámico
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Página Principal" 
        return context
    
    # Clase independiente (fuera de IndexView)
class PruebaListView(ListView):
    template_name = 'empleado/lista.html'
    queryset = ['A', 'B', 'C'] 
    context_object_name = 'lista_prueba'


class ModeloPruebaListView(ListView):
    model = Empleado
    template_name = 'empleado/lista-prueba.html'
    context_object_name = 'lista_prueba'

 
