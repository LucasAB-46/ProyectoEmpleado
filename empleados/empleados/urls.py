from django.contrib import admin
from django.urls import path, include
from applications.departamento.views import DepartamentoListView
from applications.empleado.views import (
    IndexView, sessionLogIn, sessionLogOut,
    PruebaListView,
    ListarTodosEmpleados,
    ListarEmpleadosPorDepartamento,
    EmpleadoCreateView,  
    EmpleadoUpdateView,  
    EmpleadoDeleteView,
    EmpleadoDetailView
)
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', IndexView.as_view(), name='home'),
    
    # URLs para Empleados (CRUD)
    path('empleados/', ListarTodosEmpleados.as_view(), name='empleado_list'),
    path('empleados/nuevo/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('empleados/editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    
    # URLs para Departamentos (unificadas)
    path('departamentos/', DepartamentoListView.as_view(), name='departamento_list'),
    path('lista-departamentos/', DepartamentoListView.as_view(), name='departamentos'),
    
    # Otras URLs existentes
    path('lista/', PruebaListView.as_view(), name='lista'),
    
    path('listar-por-departamento/<nombre>/', ListarEmpleadosPorDepartamento.as_view(), 
         name='lista-departamento'),
    

    path('sign-in/', sessionLogIn, name='login'),
    path('log-out/', sessionLogOut, name='logout'),
    
    # URLs para CKEditor y redirección
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=False)),
]