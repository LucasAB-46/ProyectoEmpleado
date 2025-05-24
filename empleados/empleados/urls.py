from django.contrib import admin
from django.urls import path, include
from applications.empleado.views import IndexView, PruebaListView, ModeloPruebaListView, Listar_todos_los_empleados, Listar_todos_los_empleados_por_departamento

from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', IndexView.as_view(), name='home'),  
    path('lista/',PruebaListView.as_view(), name='home'),  
    
    path('lista-prueba/', ModeloPruebaListView.as_view(), name='home'),  
    path('listar-todos-los-empleados/', Listar_todos_los_empleados.as_view()), #creo la URL
    path('listar-por-departamento/<nombre>', Listar_todos_los_empleados_por_departamento.as_view()), #creo la URL    
    

    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

] 
   