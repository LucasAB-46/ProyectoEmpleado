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

    # 1-Lista de todos los empleados de la empresa
class Listar_todos_los_empleados(ListView):
    template_name = 'empleado/listar_todos_los_empleados.html'
    model= Empleado
    #context_object_name = 'listar_todos_los_empleados'


    # 2-La lista de todos los empleados que pertenecen a un departamento especifico
class Listar_todos_los_empleados_por_departamento(ListView):
    template_name = 'empleado/listar_todos_los_empleados_por_departamento.html'
    queryset= Empleado.objects.filter(
        departamento__nombre='CONTABLE'
    )

    def get_queryset(self):
        departamento= self.kwargs['nombre']
        lista=Empleado.objects.filter(
        departamento__nombre= departamento
        )
        return lista    

    # 3-Lista de los empleados por tipo de trabajo
    # 4-Lista de empleados por algun termino de busqueda especifico
    # 5-Listar las habilidades de un empleado

    

 
